from distutils.core import setup

setup(
    name='PymageJ',
    version='0.1',
    description='Python tools for ImageJ',
    author='Jochem Smit',
    author_email='j.h.smit@rug.nl',
    url='https://github.com/Jhsmit/PymageJ/',
    packages='pymagej',
    license='GNU',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ImageJ ROI',
    install_requires=['numpy'],
)