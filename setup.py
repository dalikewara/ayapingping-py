from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ayapingping-py',
    version='4.5.4',
    python_requires='>=3.10.12',
    author='Dali Kewara',
    author_email='dalikewara@gmail.com',
    description='ayapingping-py generates standard project structure to build applications in Python that follow Clean '
                'Architecture and Feature-Driven Design concept',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords=['python', 'ayapingping', 'ayapingping-py', 'framework', 'structure', 'design', 'feature', 'project',
              'clean-architecture', 'feature-driven-design', 'domain-driven-design'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ayapingping-py = _main.main:main',
        ],
    },
)
