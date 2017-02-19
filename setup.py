from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='openfigi',
    version='0.0.4',
    description='A simple wrapper for openfigi.com',
    long_description=readme,
    author='Julian Wergieluk',
    author_email='julian@wergieluk.com',
    url='https://github.com/jwergieluk/openfigi',
    license=license,
    packages=find_packages(),
    install_requires=['requests', 'click'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    entry_points={'console_scripts': ['ofg = openfigi.__main__:call_figi']}
)
