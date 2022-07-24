from setuptools import setup

with open("README.MD", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()


setup(
    name='discord-ext-autoreload',
    author='nerdguyahmad',
    url='https://github.com/nerdguyahmad/discord-ext-autoreload',
    keywords=["discord.py", "discord", "reload", "asyncio"],
    version="0.1.1",
    packages=['discord.ext.autoreload'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    license='MIT',
    description='A discord.py extension that allows automatic hot-reloading of extensions',
    install_requires=install_requires,
    python_requires='>=3.5.3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)
