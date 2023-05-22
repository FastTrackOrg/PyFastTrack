from setuptools import setup

setup(
    name="pyfasttrack",
    version="0.0.3",
    author="Benjamin Gallois",
    author_email="benjamin.gallois@fasttrack.sh",
    description="Easy-to-use solution to integrate the tracking technology of the FastTrack software in Python projects.",
    url="https://github.com/FastTrackOrg/PyFastTrack",
    packages=['pyfasttrack'],
    install_requires=[
        'ultralytics',
        'opencv-python',
        'scipy',
        'toml',
        'sentry-sdk',
        'numpy',],
    license='MIT',
    python_requires='>=3.9',
    zip_safe=False,
)
