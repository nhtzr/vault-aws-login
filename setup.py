import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vault-aws-login",
    version="0.0.5",
    author="Ezequiel Rosas",
    author_email="ezequiel.rosas@digitalonus.com",
    description="Stay authenticated in awscli with vault",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nhtzr/vault-aws-login",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT',
    scripts=['bin/aws_credentials_merge', 'bin/vault-aws-login']
)
