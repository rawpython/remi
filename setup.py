from setuptools import setup

setup(name='remi',
      version='0.1',
      description='Python REMote Interface library',
      url='https://github.com/dddomodossola/remi',
      author='Davide Rosa',
      author_email='dddomodossola@gmail.com',
      license='Apache',
      packages=['remi', 'remi.game'],
      include_package_data=True,
	  zip_safe=False,
)
