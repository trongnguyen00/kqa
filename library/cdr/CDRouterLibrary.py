import pandas as pd
from cdrouter import CDRouter
from cdrouter.packages import Package
from cdrouter.jobs import Job
from cdrouter.results import Result
from robot.api.deco import keyword

class CDRouterLibrary():
    def __init__(self):
        self.session = None

    @keyword
    def connect_to_cdrouter(self, host, username, password):
        self.session = CDRouter(host, username=username, password=password)
        if self.session:
            return "SESSION_ESTABLISHED"
        else:
            return "SESSION_FAILED"

    @keyword
    def get_all_packages(self):
        """ 
        FIX ME
        return packages_list"""

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

    @keyword
    def delete_job(self, job_id):
        """Delete a job by ID."""
        self.session.jobs.delete(job_id)
    
    @keyword
    def edit_job(self, job_id, **kwargs):
        """Edit a job by ID.
        Some fields can be updated with dictionary: key=value.
        id(optional) Job ID as an int.

        active(optional) Bool True if status is 'running'.
        
        status(optional) Job status as a string.
        
        options(optional) jobs.Options object
        
        package_id(optional) Package ID as an int.
        
        package_name(optional) Package name as string.
        
        config_id(optional) Config ID as an int.
        
        config_name(optional) Config name as string.
        
        device_id(optional) Device ID as an int.
        
        device_name(optional) Device name as string.
        
        result_id(optional) Result ID as an int.
        
        user_id(optional) User ID as an int.
        
        created(optional) Job creation time as DateTime.
        
        updated(optional) Job last-updated time as DateTime.
        
        automatic(optional) Bool True if job scheduled automatically DateTime.
        
        run_at(optional) Job scheduled run-time DateTime.
        
        interfaces(optional) configs.Interfaces list
        
        interface_names(optional) Job interface names as string list.
        
        uses_wireless(optional) Bool True if job uses any wireless interfaces.
        
        uses_ics(optional) Bool True if job uses any ICS interfaces.
        
        ics_interface_name(optional) If uses_ics is True, ICS interface name as string.
                
        """
        job = self.session.jobs.get(job_id)
        for key, value in kwargs.items():
            setattr(job, key, value)
        return self.session.jobs.edit(job)
    
    @keyword
    def get_job_by_id(self, job_id):
        """Get a job by ID.
        returns a Job object.
        """
        return self.session.jobs.get(job_id)

    @keyword
    def get_all_jobs(self):
        """Get all jobs.
        returns a list of Job objects.
        """
        return self.session.jobs.iter_list()
    
    @keyword
    def set_launch_job(self, job_id):
        """Run a Test Package by ID.
        """
        job_obj = self.session.jobs.get(job_id)
        job_running = self.session.jobs.launch(job_obj)
    
    @keyword
    def delete_result_with_id(self, result_id):
        """Delete a result by ID."""
        self.session.results.delete(result_id)

    def _get_diff_stats_object(self, test_ids):
        """
        Get diff stats of a list of test IDs.
        test_ids: list of test IDs.
        returns a list of diff stats object.
        Must extract the attributes of the diff stats object to get detailed information.
        """
        return self.session.results.diff_stats(test_ids)
    
    @keyword
    def get_diff_test_item(self, test_ids_list):
        """
        Compare test results between two test IDs (must belong to the same package).

        Parameters:
            test_ids_list (list): A list containing exactly two test result IDs. it must be intergers.

        Returns:
            count_diff (int): Number of test items with differing results.
            df (pd.DataFrame): DataFrame showing the differing test items.
        """
        # Chuẩn bị tên cột bằng f-string
        df = pd.DataFrame(columns=[
            "Test Item",
            f"Result({test_ids_list[0]})",
            f"Result({test_ids_list[1]})"
        ])

        count_diff = 0
        diff_obj = self._get_diff_stats_object(test_ids_list)

        for test_diff in diff_obj.tests:
            if test_diff.summaries[0].result != test_diff.summaries[1].result:
                count_diff += 1
                df.loc[len(df)] = [
                    test_diff.name,
                    test_diff.summaries[0].result,
                    test_diff.summaries[1].result
                ]

        return count_diff, df

    @keyword
    def get_result_by_id(self, result_id):
        """Get a result by ID.
        returns a Result table.
        """
        result_df = pd.DataFrame(columns=[
            "Config Name",
            "Package Name",
            "Device Name",
            "Duration Test",
            "Result Message",
            "Status",
            "Pass Count",
            "Fail Count",
            "Result Directory",
            "Pause Message"
        ])
        result_obj = self.session.results.get(result_id)
        result_df.loc[len(result_df)] = [
            result_obj.config_name,
            result_obj.package_name,
            result_obj.device_name,
            result_obj.duration,
            result_obj.result,
            result_obj.status,
            result_obj.passed,
            result_obj.fail,
            result_obj.result_dir,
            result_obj.pause_message
        ]

        return result_df

    @keyword
    def get_all_results(self):
        """Get all results.
        returns a list of Result objects.
        """
        df = pd.DataFrame(columns=[
            "Config Name",
            "Package Name",
            "Device Name",
            "Duration Test",
            "Result Message",
            "Status",
            "Pass Count",
            "Fail Count",
            "Result Directory",
            "Pause Message"
        ])
        for result_obj in self.session.results.iter_list():
            df.loc[len(df)] = [
                result_obj.config_name,
                result_obj.package_name,
                result_obj.device_name,
                result_obj.duration,
                result_obj.result,
                result_obj.status,
                result_obj.passed,
                result_obj.fail,
                result_obj.result_dir,
                result_obj.pause_message
            ]
        return df

    @keyword
    def set_lock_result(self, result_id):
        """set lock to a result."""
        return self.session.results.lock(result_id)
    
    @keyword
    def set_unlock_result(self, result_id):
        """set unlock to a result."""
        return self.session.results.unlock(result_id)

    @keyword
    def set_pause_result(self, result_id):
        """set pause to a result."""
        return self.session.results.pause(result_id)

    @keyword
    def set_unpause_result(self, result_id):
        """set resume to a result."""
        return self.session.results.unpause(result_id)

    @keyword
    def stop_running_result(self, result_id):
        """stop running a result."""
        return self.session.results.stop(result_id)

    @keyword
    def get_list_test_result(self, result_id):
        """get summary of a result."""
        df = pd.DataFrame(columns=[
            "Sequence",
            "Name",
            "Result",
            "Skip Reason",
            "Description"
        ])
        summaries = self.session.results.summary_stats(result_id)

        for var in summaries.test_summaries:
            df.loc[len(df)] = [
                var.seq,
                var.name,
                var.result,
                var.skip_reason,
                var.description
            ]
        return df