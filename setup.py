import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="handwritten-text-recognition",
    version="0.0.1",
    author="Arthur Flor, Jan R.",
    author_email="author@example.com",
    description="Package to create handwritten text recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurflor23/handwritten-text-recognition",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=['imageio', 'editdistance', 'kaldiio',
    #                   'numba', 'opencv-python'], # 'opencv-python>=4.1.2.30', 'tensorflow>=2.1.0'
)
