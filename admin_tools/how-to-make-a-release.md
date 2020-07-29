# Get latest sources:

    $ git pull

# Change version in FoxySheep/version.py.

    $ emacs FoxySheep/version.py
    $ source FoxySheep/version.py
    $ echo $VERSION
    $ git commit -m"Get ready for release $VERSION" .


# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS.md from ChangeLog. Then:

    $ emacs NEWS.md
    $ git commit --amend .
    $ git push   # get CI testing going early

# Make distribution

    $ make dist
	$ twine check dist/FoxySheep-$VERSION*

# Check package on github

	$ [[ ! -d /tmp/gittest ]] && mkdir /tmp/gittest; pushd /tmp/gittest
	$ pyenv local 3.8.4
	$ pip install -e git://github.com/rocky/FoxySheep.git#egg=FoxySheep
	$ foxy-sheep --version
	$ foxy-sheep -e '1+2 3'
	$ pip uninstall FoxySheep
	$ popd

# Release on Github

Goto https://github.com/rocky/FoxySheep2/releases/new

Now check the *tagged* release. (Checking the untagged release was previously done).

Todo: turn this into a script in `admin-tools`

	$ pushd /tmp/gittest
	$ pip install -e git://github.com/rocky/FoxySheep.git@$VERSION#egg=xdis
	$ foxy-sheep --version
	$ pip uninstall FoxySheep
	$ popd


# Get on PyPI

	$ twine upload dist/FoxySheep-${VERSION}*

Check on https://pypi.org/project/FoxySheep/

# Pull tags:

    $ git pull --tags

# Move dist files to uploaded

	$ mv -v dist/FoxySheep-${VERSION}* dist/uploaded
