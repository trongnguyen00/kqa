import pandas as pd
import time
from robot.api import logger
from cdrouter import CDRouter
from cdrouter.packages import Package
from cdrouter.jobs import Job
from cdrouter.results import Result
from cdrouter.devices import Device
from robot.api.deco import keyword

class CDRouterLibrary():
    def __init__(self):
        self.session = None

    # CONNECTION
    @keyword
    def connect_to_cdrouter(self, host, username, password):
        self.session = CDRouter(host, username=username, password=password)
        if self.session:
            return "SESSION_ESTABLISHED"
        else:
            return "SESSION_FAILED"

    # PACKAGES
    @keyword
    def get_all_packages_info(self):
        """ return a dataframe contain info of all packages"""
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Test Count",
            "Configuration",
            "Device"
        ])
        for item in self.session.packages.iter_list():
            df.loc[len(df)] = [
                item.id,
                item.name,
                item.description,
                item.test_count,
                item.config_id,
                item.device_id
            ]
        return df

    @keyword
    def get_package_by_id(self, package_id):
        """return a package object
        """
        return self.session.packages.get(package_id)

    @keyword
    def get_package_info_by_id(self, package_id):
        """return a package info table
        """
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Test Count",
            "Configuration",
            "Device"
        ])
        package_obj = self.session.packages.get(package_id)
        df.loc[len(df)] = [
            package_obj.id,
            package_obj.name,
            package_obj.description,
            package_obj.test_count,
            package_obj.config_id,
            package_obj.device_id
        ]
        return df
    
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
    def get_package_info_by_name(self, name):
        """Get a test package by name.
        returns a Package object.
        """
        pkg = self.session.packages.get_by_name(name)
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Test Count",
            "Configuration",
            "Device"
        ])
        config_obj = self.session.configs.get(pkg.config_id).name
        device_obj = self.session.devices.get(pkg.device_id).name
        
        df.loc[len(df)] = [
            str(pkg.id),
            pkg.name,
            pkg.description,
            str(pkg.test_count),
            config_obj,
            device_obj
        ]
        return df

    @keyword
    def get_package_id_by_name(self, name):
        """Get a test package ID by name.
        returns a Package ID.
        """
        pkg = self.session.packages.get_by_name(name)
        return pkg.id if pkg else None
    
    @keyword
    def create_package(self, name, description=''):
        """Create a new Test Package.
        Returns a Package object."""
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
        """share a package to list of user.
        Return a list shared user IDs.
        """
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

    # JOBS

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
    def set_launch_job(self, package_id, **kwargs):
        """Run a Test Package by ID.
        Run this package then return job id
        """
        job_obj = Job(
            package_id=package_id,
            **kwargs
        )

        job_running = self.session.jobs.launch(job_obj)

        return job_running.id

    @keyword
    def get_package_name_from_job(self, job_id):
        """Get package name from a job ID.
        returns a Package name.
        """
        job_obj = self.session.jobs.get(job_id)
        return job_obj.package_name

    def get_device_name_from_job(self, job_id):
        """Get device name from a job ID.
        returns a Device name.
        """
        job_obj = self.session.jobs.get(job_id)
        return job_obj.device_name
    
    def get_result_id_from_job(self, job_id):
        """Get result ID from a job ID.
        returns a Result ID.
        """
        job_obj = self.session.jobs.get(job_id)
        return job_obj.result_id

    def get_config_name_from_job(self, job_id):
        """Get config name from a job ID.
        returns a Config name.
        """
        job_obj = self.session.jobs.get(job_id)
        return job_obj.config_name

    def get_job_status(self, job_id):
        """Get job status from a job ID.
        returns a Job status.
        """
        job_obj = self.session.jobs.get(job_id)
        return job_obj.status

    def check_until_job_completed(self, job_id):
        """Check if a job is completed.
        """
        While True:
            job_obj = self.session.jobs.get(job_id)
            status = job_obj.status
            if status == 'completed':
                logger.info(f"Job {job_id} is completed.")
                return True
            elif status in ['error', 'stopped']:
                logger.info(f"Job {job_id} is not completed. Status: {status}")
                BuildIn().fail(f"Job {job_id} is not completed. Status: {status}")
            elif status in ['running', 'pending']:
                logger.info(f"Job {job_id} is still running. Status: {status}")
                time.sleep(10)
            else:
                BuildIn().fail(f"Job {job_id} has an unknown status: {status}")
        
    # RESULTS

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
    
    # DEVICES
    @keyword
    def set_create_device(self, name, model_name, **kwargs):
        """Create a new Device.
        Valid key:
        - id (optional) Device ID as an int.
        - name (optional) Name as string.
        - created (optional) Creation time as DateTime.
        - updated (optional) Last-updated time as DateTime.
        - locked (optional) Bool True if device is locked.
        - user_id (optional) User ID as an int.
        - result_id (optional) Result ID as an int (if a device snapshot).
        - attachments_dir (optional) Filepath for attachments as string.
        - picture_id (optional) Attachment ID for used for device picture as an int.
        - tags (optional) Tags as string list.
        - default_ip (optional) Default IP as a string
        - default_login (optional) Default login as a string
        - default_password (optional) Default password as a string
        - default_ssid (optional) Default SSID as a string
        - location (optional) Location as a string
        - device_category (optional) Device category as a string
        - manufacturer (optional) Manufacturer as a string
        - manufacturer_oui (optional) Manufacturer OUI as a string
        - model_name (optional) Model name as a string
        - model_number (optional) Model number as a string
        - description (optional) Description as a string
        - product_class (optional) Product class as a string
        - serial_number (optional) Serial number as a string
        - hardware_version (optional) Hardware version as a string
        - software_version (optional) Software version as a string
        - provisioning_code (optional) Provisioning code as a string
        - note (optional) Note as a string
        - insecure_mgmt_url (optional) True if insecure HTTPS management URLs are allowed
        - mgmt_url (optional) Management URL as a string
        - add_mgmt_addr (optional) True if address should be configured when opening proxy connection
        - mgmt_interface (optional) Interface on which to configure address as string
        - mgmt_addr (optional) Address to configure as string
        - power_on_cmd (optional) Command to run to power on device as string
        - power_off_cmd (optional) Command to run to power off device as string"""
        dev_obj = Device(
            name=name,
            model_name=model_name,
            **kwargs
        )
        device = self.session.devices.create(dev_obj)
        return device
    
    @keyword
    def set_delete_device(self, device_id):
        """Delete a Device by ID."""
        self.session.devices.delete(device_id)

    @keyword
    def set_update_device(self, device_id, **kwargs):
        """Edit a Device based on ID. Return a Device updated object.
        Valid key:
        - id (optional) Device ID as an int.
        - name (optional) Name as string.
        - created (optional) Creation time as DateTime.
        - updated (optional) Last-updated time as DateTime.
        - locked (optional) Bool True if device is locked.
        - user_id (optional) User ID as an int.
        - result_id (optional) Result ID as an int (if a device snapshot).
        - attachments_dir (optional) Filepath for attachments as string.
        - picture_id (optional) Attachment ID for used for device picture as an int.
        - tags (optional) Tags as string list.
        - default_ip (optional) Default IP as a string
        - default_login (optional) Default login as a string
        - default_password (optional) Default password as a string
        - default_ssid (optional) Default SSID as a string
        - location (optional) Location as a string
        - device_category (optional) Device category as a string
        - manufacturer (optional) Manufacturer as a string
        - manufacturer_oui (optional) Manufacturer OUI as a string
        - model_name (optional) Model name as a string
        - model_number (optional) Model number as a string
        - description (optional) Description as a string
        - product_class (optional) Product class as a string
        - serial_number (optional) Serial number as a string
        - hardware_version (optional) Hardware version as a string
        - software_version (optional) Software version as a string
        - provisioning_code (optional) Provisioning code as a string
        - note (optional) Note as a string
        - insecure_mgmt_url (optional) True if insecure HTTPS management URLs are allowed
        - mgmt_url (optional) Management URL as a string
        - add_mgmt_addr (optional) True if address should be configured when opening proxy connection
        - mgmt_interface (optional) Interface on which to configure address as string
        - mgmt_addr (optional) Address to configure as string
        - power_on_cmd (optional) Command to run to power on device as string
        - power_off_cmd (optional) Command to run to power off device as string"""
        dev_obj = self.session.devices.get(device_id)
        for key, value in kwargs.items():
            if hasattr(dev_obj, key):
                setattr(dev_obj, key, value)
            else:
                print(f"Warning: '{key}' is not a valid attribute of Device")
        
        updated_dev = self.session.devices.edit(dev_obj)
        return updated_dev

    def get_device_by_id(self, device_id):
        """Get a Device by ID.
        returns a Device object.
        """
        return self.session.devices.get(device_id)

    @keyword
    def get_device_id_by_name(self, name):
        """Get a Device ID by name.
        returns a Device ID.
        """
        device = self.session.devices.get(name)
        return device.id if device else None

    @keyword
    def get_device_by_name(self, name):
        """Get a Device by name.
        returns a Device object.
        """
        return self.session.devices.get_by_name(name)

    @keyword
    def get_all_devices_info(self):
        """Get all Devices.
        returns a list of Device objects.
        """
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Model Name",
            "Serial Number",
            "Product Class",
            "Default Ip",
            "Default Login",
            "Default Password",
            "Lock State",
        ])

        dev_list = self.session.devices.iter_list()
        for dev in dev_list:
            df.loc[len(df)] = [
                dev.id,
                dev.name,
                dev.description,
                dev.model_name,
                dev.serial_number,
                dev.product_class,
                dev.default_ip,
                dev.default_login,
                dev.default_password,
                dev.locked
            ]
        return df

    @keyword
    def set_lock_device(self, device_id):
        """set lock to a device."""
        return self.session.devices.lock(device_id)

    @keyword
    def set_unlock_device(self, device_id):
        """set unlock to a device."""
        return self.session.devices.unlock(device_id)

    @keyword
    def set_power_on_device(self, device_id):
        """set power on to a device."""
        return self.session.devices.power_on(device_id) 

    @keyword
    def set_power_off_device(self, device_id):
        """set power off to a device."""
        return self.session.devices.power_off(device_id)

    # CONFIGS
    @keyword
    def set_create_config(self, name, **kwargs):
        """Create a new Config. return a Config object.
        Valid key:
        id (optional) Config ID as an int.
        name (optional) Config name as string.
        description (optional) Config description as string.
        created (optional) Creation time as DateTime.
        updated (optional) Last-updated time as DateTime.
        locked (optional) Bool True if config is locked.
        contents (optional) Config contents as string.
        user_id (optional) User ID as an int.
        result_id (optional) Result ID as an int (if a config snapshot).
        tags (optional) Tags as string list.
        note (optional) Note as string.
        interfaces (optional) configs.Interfaces list (if a config snapshot).
        nta_platform (optional) Config NTA platform as string.
        """

        config_obj = Config(name=name, **kwargs)
        config_profile = self.session.configs.create(config_obj)
        return config_profile

    @keyword
    def set_delete_config(self, config_id):
        """Delete a Config by ID."""
        self.session.configs.delete(config_id)

    @keyword
    def modify_config(self, config_id, **kwargs):
        """Edit a Config based on ID. Return a Config updated object.
        Valid key:
        id (optional) Config ID as an int.
        name (optional) Config name as string.
        description (optional) Config description as string.
        created (optional) Creation time as DateTime.
        updated (optional) Last-updated time as DateTime.
        locked (optional) Bool True if config is locked.
        contents (optional) Config contents as string.
        user_id (optional) User ID as an int.
        result_id (optional) Result ID as an int (if a config snapshot).
        tags (optional) Tags as string list.
        note (optional) Note as string.
        interfaces (optional) configs.Interfaces list (if a config snapshot).
        nta_platform (optional) Config NTA platform as string.
        """
        config_obj = self.session.configs.get(config_id)
        for key, value in kwargs.items():
            setattr(config_obj, key, value)
        
        updated_config = self.session.configs.edit(config_obj)
        return updated_config

    @keyword
    def get_config_by_id(self, config_id):
        """Get a Config by ID.
        returns a Config object.
        """
        return self.session.configs.get(config_id)

    @keyword
    def get_config_info_by_name(self, name):
        """Get a Config by name.
        returns a Config object.
        """
        config_obj = self.session.configs.get_by_name(name)
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Lock State"
        ])
        df.loc[len(df)] = [
            config_obj.id,
            config_obj.name,
            config_obj.description,
            config_obj.locked
        ]
        return df

    @keyword
    def get_config_by_name(self, name):
        """Get a Config by name.
        returns a Config object.
        """
        return self.session.configs.get_by_name(name)

    @keyword
    def get_config_content(self, config_id):
        """Get a Config content by ID.
        returns a Config content as string.
        """
        return self.session.configs.get_plaintext(config_id)

    @keyword
    def get_interfaces_in_config(self, config_id):
        """Get a Config interfaces by ID.
        returns a Config interfaces in config content.
        """
        df = pd.DataFrame(columns=[
            "Name",
            "Value",
            "Is Wireless"
        ])

        content_plain = self.session.configs.get_plaintext(config_id)
        interfaces_info = self.session.configs.get_interfaces(content_plain)
        for interface in interfaces_info:
            df.loc[len(df)] = [
                interface.name,
                interface.value,
                interface.is_wireless
            ]

        return df
    
    @keyword
    def get_all_configs_info(self):
        """Get all Configs.
        returns a list of Config objects.
        """
        df = pd.DataFrame(columns=[
            "ID",
            "Name",
            "Description",
            "Lock State"
        ])

        config_list = self.session.configs.iter_list()
        for config in config_list:
            df.loc[len(df)] = [
                config.id,
                config.name,
                config.description,
                config.locked
            ]
        return df

    @keyword
    def get_all_testvar_value(self, config_id):
        """Get all test variables in a Config.
        returns a list of test variables.
        """
        df = pd.DataFrame(columns=[
            "Name",
            "Current Value",
            "Group",
            "Default Value",
            "Is Default",
        ])
        testvars = self.session.configs.list_testvars(config_id)
        for testvar in testvars:
            df.loc[len(df)] = [
                testvar.name,
                testvar.value,
                testvar.group,
                testvar.default,
                testvar.is_default
            ]

        return df

    @keyword
    def set_lock_config(self, config_id):
        """set lock to a config."""
        return self.session.configs.lock(config_id)

    @keyword
    def set_unlock_config(self, config_id):
        """set unlock to a config."""
        return self.session.configs.unlock(config_id)