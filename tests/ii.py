import os
pet_photo = 'images/Cat2.jpg'
pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
print(pet_photo)
