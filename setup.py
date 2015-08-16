from distutils.core import setup

setup(
    name='PymageJ',
    version='0.1',
    description='Python tools for ImageJ',
    author='Jochem Smit',
    author_email='j.h.smit@rug.nl',
    url='https://github.com/Jhsmit/PymageJ/',
    download_url='https://github.com/Jhsmit/PymageJ/tarball/0.1',
    packages=['PymageJ'],
    license='GNU',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ImageJ ROI',
    requires=['numpy']
)
