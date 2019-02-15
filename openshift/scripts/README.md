# OpenShift Scripts

A set of helper scripts to help maintain the project.

## commonFunctions.inc

A set of common functions to include in your scripts.

## createGlusterfsClusterApp.sh

Create/re-create the Gluster file system resources on a project.

## createLocalProject.sh

Creates an project on a local OpenShift cluster.

## deleteLocalProject.sh

Deletes an project from a local OpenShift cluster.

## dropAndRecreateDatabase.sh

A helper script to drop and recreate the application database within a given environment.

Refer to the usage documentation contained in the script for details.  Run the script without parameters to see the documentation.

_This script could be further enhanced to utilize the environment variables within the running pod to determine various database parameters dynamically.  The process will require some fussing around with escaping quotes and such to get things just right._

## getPodByName.sh

A utility script that returns the full name of a running instance of a pod, given the pod's name and optionally the pod index.

Refer to the usage documentation contained in the script for details.  Run the script without parameters to see the documentation.

## grantDeploymentPrivileges.sh

Grants deployment configurations access to the images in the tools project.

## runInContainer.sh

This script is a wrapper around `oc exec` that allows you to run commands inside a pod instance based on it's general name.

Refer to the usage documentation contained in the script for details.  Run the script without parameters to see the documentation.

## scaleDeployment.sh

A helper scrript to scale a deployment to a particular number of pods.

## tagProjectImages.sh

Tags the project's images, as defined in the project's settings.sh file.

## ToDo:

Generate additional scripts that automate the process reloading the data for an application.  Such a process is documented here; [Detailed Steps to reset the Database for an environment](https://github.com/bcgov/hets/tree/master/APISpec/TestData#detailed-steps-to-reset-the-database-for-an-environment).

Needed are:

- A script to find a replication controller by name, similar to `getPodByName.sh`.
  - The following oc command gets us part way there;
    - `oc get rc -l "openshift.io/deployment-config.name=schema-spy" --template "{{ with index .items (len .items) }}{{ .metadata.name }}{{ end }}"`
  - It actually points one index past the active replication controller.  Unfortunately I have not found a way to do math in the template to subtract 1 from the index to get the active controller.
- A script to scale the replication controller(s) for the main application (the one controlling the database migrations) up and down.
- A wrapper script to then combine the steps together; 1. Scale Down, 2. Recreate Database. 3. Scale Up.
- A top level script to combine the above operations with the data loading process (which is controlled by another set of existing scripts).
