from setuptools import setup

setup(name="enetcomponents", version="0.1.0", author="Manuel cortez", author_email="manuel@manuelcortez.net", url="https://code.manuelcortez.net/manuelcortez/enet-client-server", packages=["enetcomponents"], long_description=open("readme.md", "r").read(), description="Enet components to make client-server communication a bit easier.", install_requires=["pyenet"])