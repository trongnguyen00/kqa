from cdrouter import CDRouter
from robot.api.deco import keyword

class CDRouterLibrary:
    def __init__(self):
        self.session = None

    @keyword
    def connect_to_cdrouter(self, host, username, password):
        self.session = CDRouter(hostname=host, username=username, password=password)
        if self.session:
            return "SESSION_ESTABLISHED"
        else:
            return "SESSION_FAILED"

    @keyword
    def get_all_packages(self):
        """ return packages_list"""
        return self.session.packages.iter_list()

    @keyword
    def get_package_by_id(self, package_id):
        """return a package object"""
        return self.session.packages.get(package_id)
    
    @keyword
    def get_all_id_packages(self):
        """Get id of all packages in a list of Package objects.
        Rerturn a list of package IDs.
        """
        return [pkg.id for pkg in self.session.packages.iter_list()]
    
    @keyword
    def get_all_name_packages(self):
        """Get name of all packages in a list of Package objects.
        Rerturn a list of package names.
        """
        return [pkg.name for pkg in self.session.packages.iter_list()]

    @keyword
    def get_package_by_name(self, name):
        """Get a test package by name.
        returns a Package object.
        """
        return self.session.packages.get_by_name(name)
    
    @keyword
    def get_package_id_by_name(self, name):
        """Get a test package ID by name.
        returns a Package ID.
        """
        pkg = self.session.packages.get_by_name(name)
        return pkg.id if pkg else None
    
    @keyword
    def create_package(self, name, description=''):
        """Create a new Test Package."""
        pkg = self.session.packages.create(name=name, description=description)
        return pkg
    
    @keyword
    def set_update_package(self, package_id, **kwargs):
        """Update Test Package.
        Some fields can be updated with dictionary: key=value.
        id(optional) Package ID as an int.

        name(optional) Name as a string.

        description(optional) Description as a string.

        created(optional) Creation time as DateTime.

        updated(optional) Last-updated time as DateTime.

        locked(optional) Bool True if package is locked.

        test_count(optional) Test count as an int.

        testlist(optional) Testlist as a string list.

        extra_cli_args(optional) Extra CLI args as a string.

        user_id(optional) User ID as an int.

        agent_id(optional) Agent ID as an int.

        config_id(optional) Config ID as an int.

        result_id(optional) Result ID as an int (if a package snapshot).

        device_id(optional) Device ID as an int.

        options(optional) packages.Options object

        tags(optional) Tags as a string list.

        use_as_testlist(optional) Bool True if package is used as a testlist.

        note(optional) Note as a string.

        schedule(optional) packages.Schedule object

        interfaces(optional) configs.Interfaces list (if a package snapshot).
        """
        pkg = self.session.packages.get(package_id)
        for key, value in kwargs.items():
            setattr(pkg, key, value)
        return self.session.packages.edit(pkg)
    
    @keyword
    def delete_package(self, package_id):
        """Delete Test Package by ID."""
        self.session.packages.delete(package_id)

    @keyword
    def set_shared_package(self, package_id, user_ids):
        """share a package to list of user."""
        return self.session.packages.edit_shares(package_id, user_ids)

    @keyword
    def get_shared_package(self, package_id):
        """get shared users of a package."""
        return self.session.packages.get_shares(package_id)

    @keyword
    def set_lock_package(self, package_id):
        """set lock to a package."""
        return self.session.packages.lock(package_id)

    @keyword
    def set_unlock_package(self, package_id):
        """set unlock to a package."""
        return self.session.packages.unlock(package_id)

    @keyword
    def get_all_test_in_package(self, package_id):
        """get all tests in a package.
        Return a list of all tests in a package, with any addons, modules or testlists expanded.
        """
        return self.session.packages.testlist_expanded(package_id)