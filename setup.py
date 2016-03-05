from setuptools import setup

setup(name='remi',
      version='0.1',
      description='Python REMote Interface library',
      url='https://github.com/dddomodossola/remi',
      author='Davide Rosa',
      author_email='dddomodossola@gmail.com',
      license='Apache',
      packages=['remi','editor'],
      package_dir={'remi':'remi', 'editor':'editor'},
      package_data={'remi': ['res/*.*'],'editor': ['res/*.*']},
      include_package_data=True,
)