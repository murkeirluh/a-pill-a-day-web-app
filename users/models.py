from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from random import choice

first = ['dangerous', 'vulnerable', 'scrawny', 'equal', 'receptive', 'fragrant', 'purring', 'cavernous', 'reassuring', 'brisk', 'panoramic', 'awake', 'incisive', 'trivial', 'quiet', 'fickle', 'auspicious', 'broad', 'rosy', 'peevish', 'guarded', 'satisfying', 'musical', 'staid', 'illiterate', 'mediocre', 'vigilant', 'true', 'squiggly', 'taboo', 'fallacious', 'meek', 'tame', 'revolving', 'womanly', 'classic', 'wilted', 'infantile', 'equatorial', 'tan', 'unlawful', 'meddlesome', 'standing', 'rebel', 'apt', 'acidic', 'tattered', 'royal', 'cooing', 'ceaseless', 'hurried', 'nutritious', 'variable', 'leery', 'courteous', 'godly', 'uptight', 'next', 'violent', 'worthwhile', 'sizzling', 'dowdy', 'lavish', 'grand', 'heavenly', 'seemly', 'smooth', 'worst', 'cheery', 'lying', 'clueless', 'faded', 'dynamic', 'evasive', 'futuristic', 'extraneous', 'secretive', 'judgmental', 'crass', 'bitter', 'frivolous']
second = ['fibula', 'raisins', 'paella', 'brain', 'phalanges', 'crackers', 'tendon', 'artery', 'mayonnaise', 'zygomatic', 'vein', 'bone', 'medulla', 'cake', 'lobe', 'arm', 'metatarsal', 'rice', 'icecream', 'hormones', 'pepperoni', 'vocal', 'quiche', 'milkshakes', 'epidermis', 'organ', 'pepper', 'oblongata', 'chowder', 'nucleus', 'doughnut', 'collarbone', 'garlic', 'pear', 'basmati', 'tomatoe', 'abalone', 'cheese', 'wrist', 'torso', 'medial', 'ovary', 'orange', 'femur', 'limbic', 'salami', 'sardines', 'pistachio', 'vegetables', 'forearm', 'anus', 'teeth', 'jugular', 'heart', 'buttocks', 'venison', 'dna', 'tacos', 'uvula', 'humor', 'joint', 'wrinkles', 'cranium', 'socket', 'mammary', 'cerebrum', 'syrup', 'granola', 'vitreous', 'xiphoid', 'triceps', 'meniscus', 'ears', 'gyrus', 'ankle', 'muesli', 'deltoid', 'truffle', 'oil', 'face', 'relish', 'gatorade', 'apricots', 'diaphragm', 'apples', 'lard', 'nodule', 'cordial', 'polenta', 'blood', 'palate', 'disc', 'clam', 'pudding', 'carpus', 'jowl', 'groin', 'posterior', 'lollies', 'oatmeal', 'jerky', 'caviar', 'sternum', 'womb', 'vessels', 'aorta', 'marrow', 'sausage', 'tibia', 'retina', 'tubes', 'salt', 'eggs', 'tissue', 'tongue', 'iris', 'lumbar', 'septum', 'calf', 'bagels', 'burritos', 'chile', 'coconut', 'molar', 'thumb', 'chest', 'pelvis', 'dermis', 'navel', 'shoulders', 'pie', 'pretzels', 'quadriceps']

def generate_key():
    chars = [chr(i) for i in range(ord('a'), ord('z')+1)]
    chars.extend([chr(i) for i in range(ord('A'), ord('Z')+1)])
    chars.extend([str(i) for i in range(10)])
    key = ''

    for i in range(6):
        key += choice(chars)

    return key

""" Generates a random username """
def random_username():
    return str(choice(first)) + str(choice(second))

""" Creates users """
class BaseUserManager(BaseUserManager):
    
    """ Creates doctor / patient accounts """
    def create_user(self, username, user_type, password=None):
        if not username:
            username = random_username()
        
            while self.model.objects.filter(username=username).first():
                username = random_username()
        
        user = self.model(username=username, user_type=user_type)

        user.set_password(password)
        user.save(using=self._db)

        return user

    """ Creates admin accounts """
    def create_super_user(self, username, password):
        user = self.create_user(username=username, user_type="admin", password=password)
        user.save(using=self._db)

        return user

class BaseUser(AbstractBaseUser):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    user_type = models.CharField(max_length=20, null=False)
    objects = BaseUserManager()
    
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def get_id(self):
        return self.user_id

    def __str__(self):
        return self.username

# class KeyManager(models.Manager):
#     def create_key(self, key=None):
#         try:
#             genkey = self.model(text=(key if key is not None else generate_key()))
#         except:
#             key = generate_key()
#             while Keys.objects.filter(text=key).first():
#                 key = generate_key()
#             genkey = self.model(text=key)
#         genkey.save(using=self._db)
        
#         return genkey

# class Keys(models.Model):
#     gen_id = models.AutoField(primary_key=True)
#     text = models.CharField(max_length=6, unique=True)
#     created = models.DateField(auto_now_add=True)

#     objects = KeyManager()

#     def __str__(self):
#         return self.text

#     def get_id(self):
#         return self.gen_id

#     def get_text(self):
#         return self.text


class AdminManager(models.Manager):
    def create_admin(self, username, password, name):
        if not username:
            username = random_username()
        
            while self.model.objects.filter(username=username).first():
                username = random_username() 

        user = BaseUser.objects.create_superuser(username, password)
        admin_details = self.model(user=user, name=name)
        admin_details.save()

        return admin_details 

# administrators - user_id, name
class Administrators(models.Model):
    user = models.OneToOneField(BaseUser, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)

    objects = AdminManager()

    def __str__(self):
        return 'Admin #{}: {}'.format(self.admin_id, self.name)

# users - id, username, password, type, date_created, date_deleted, date_modified
class DoctorsManager(models.Manager):
    def create_doctor(self, username, name, specialization, password=None):
        if not username:
            username = random_username()
        
            while self.model.objects.filter(username=username).first():
                username = random_username()
        
        user = BaseUser.objects.create_user(username, "doctor", password)
        doctor_details = self.model(user=user, name=name, specialization=specialization)
        doctor_details.save()

        return doctor_details 

# doctors - user_id, doctor_id, name, specialization, gen_id
class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    specialization = models.CharField(max_length=255, null=False)

    objects = DoctorsManager()

    def __str__(self):
        return 'Doctor #{}: {}'.format(self.doctor_id, self.name)

class PatientsManager(models.Manager):
    def create_patient(self, username, doctor, name,  password=None):
        if not username:
            username = random_username()
        
            while self.model.objects.filter(username=username).first():
                username = random_username()
        
        user = BaseUser.objects.create_user(username, "patient", password)
        
        patient_details = self.model(user=user, doctor=doctor, name=name)
        patient_details.save()

        return patient_details 

# patients - user_id, patient_id, doctor_id, name, gen_id, slug'''
class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)

    objects = PatientsManager()
    
    def __str__(self):
        return 'Patient #{} by Doctor #{}'.format(self.patient_id, self.doctor_id)
    