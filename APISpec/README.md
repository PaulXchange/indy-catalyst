# TheOrgBook - API Specification

TheOrgBook data model is designed around claims collection and searching using a search engine (Solr) indexed on Organization Names (Legal and Doing Business As - DBA), location (address and spatial) and claims held (boolean - not the contents of the claims).  The current design is that as Claims for organizations are received, the organization Business Id, Name, Address and claim status are extracted from the claim and put into tables in the database. As well the JSON-LD that is the claim itself is also put into a column in the database. The claim is not itself indexed as part of the searchable content - just the extracted data from processing the claim.

The basic API around the data model was initially defined to be just the CRUD operations for the entities that make up the data model - GET, POST, PUT, GET by Id and Bulk Load. In addition, a search API invoking SOLR has been added to the API and additional endpoints will be added as needed to support the API, and the Service Agent-to-TheOrgBook operations. The API can, where possible, call external APIs for capabilities such as address cleanup.

The Data Model includes entities supporting Users, Roles and Permissions. Currently, no authentication or authorization has been implemented, although that is possible.

# API Specification Management - Overview

This folder contains the OpenAPI/Swagger files that define the API for the TheOrgBook Front End Client calling the TheOrgBook API Server.  Swagger files can become very large.  This repo uses method to allow the API definition to be easily edited to minimize human error, and increase accessibility to editing the specification. This readme documents the mechanism we are using in TheOrgBook to use a specially formatted Excel file to produce the TOBSwagger.yaml file for the application. We subsequently use the yaml file as input to extended Swagger code generators to produce significant chunks of the application code.

## Setup

Before you can make changes to the API Spec you will need the following installed on your computer:

- git: required to clone the project repository and commit changes.
- Microsoft Excel:  Office 365 / Excel 2016 is version currently used to edit the Excel file. Note that the file contains a macro that is pretty important to the process and you must be able to run that macro.
- python 2.7: required to convert .CSV to .JSON
- mustache: required to convert .JSON to .YAML.  The Node.js implementation of mustache is recommended; other variants may not support the specific syntax used in the mustache files for this project.
- swagger-cli: optional but very useful to validate the resulting swagger.

See [swagger-cli](https://www.npmjs.com/package/swagger-cli) to download
  - To Do: Create/find a docker version of this so it can be run directly without installation.

This project uses a code generator from the projects [Swagger-Codegen](https://github.com/swagger-api/swagger-codegen) [Swagger-Codegen-Extension](https://github.com/bcgov/Swagger-Codegen-Extension). The jars in this folder are from those projects. Unlikely, however, it may be useful to grab updated versions of those files for the application, if they have been updated with features useful to this project.

## Excel Input

The Excel master file is located at the repository location APISpec/in/TOBSwagger.xlsm

Macros are used in the file, so must be enabled after loading the file into Excel.

In order to provide an easy interface to editing the data, an Excel spreadsheet is used.  This spreadsheet has the following sheets in it:

- defs.csv: model definitions.  One row per entity column.
- paths.csv: API paths.  One row per endpoint - or set of endpoints (for crud)
- model.csv: Converts defs.csv to a model definition.
- api.csv: Converts paths.csv to a API definition.

Through the generation process (described below), two YAML files are generated from this data - model.yaml (containing the data model) and api.yaml (containing the REST API calls).

## Export From Excel

Once all changes to the Excel spreadsheet have been completed, the contents of the excel spreadsheet must be exported as CSV files.  Use the keyboard sequence CTRL-SHIFT-V to run a macro which will rapidly save each sheet tagged for export as a CSV file. Or do it manually. Uggghh.

The specific macro that the key combination calls is Save2CSV; it simply loops through the sheets in the workbook and saves each sheet with a name ending in .csv to a .csv file.

## Custom Swagger Sections

A provision is available for custom sections in the Swagger yaml.  This allows for uncommon API paths, user view models and other material that is not generated from the excel data.

Special files are:

- **header.yaml**: Text that appears at the top of the swagger file.  Typically includes the license, project name and other details.
- **postapi.yaml**:  Custom paths that will go below the generated API paths (api.yaml).  Often used for special services that are not common patterns.
- **footer.yaml**: Text that appears at the bottom of the swagger file after the models (model.yaml).  May include view models, security definitions and other text that goes below the model definition.

## Swagger File Assembly

The script "mkswagger.bat" is a Windows batch file which processes the output of the Export From Excel step. "mkswagger.sh" is a Linux bash shell equivalent. Neither scripts take arguments and expect the CSV files to have already been generated from the excel. Make sure to run the export CSV macro from within Excel.

*To Do: Work has started on an Excel to JSON converter so we can skip the CSV macro and the manual export step.*

The scripts does the following:

1. Converts the .CSV files generated by the Export From Excel step to .JSON
2. Uses Mustache templates with the JSON data as an input, generate .YAML fragments for the model and API paths
3. Backs up the current TOBSwagger.yaml to TOBSWagger.yaml.bck.  This is done so that a visual diff tool (e.g. winmerge on Windows) can be used to review the changes and to verify they are as you expect them to be - a good practice.
4. Combines the generated .YAML fragments with static hand edited fragments into TOBSwagger.yaml.


* To Do: Add a possibly optional call to *swagger validate TOBSwagger.yaml* to verify the output. The swagger validate output is brutal to deal with. It does show errors, but is not particularly helpful in solving the problems in the Swagger file.

## Troubleshooting the generated Swagger File

Common problems are:

- Invalid characters in the CSV/JSON/YAML files cause the file assembly or code generation to fail.
- Mismatched object relationships in the definitions (e.g. an entity is renamed in the model, but the old name is referenced elsewhere in the file)

In the event that the input data is unparsable, and no output file is created, review the output from the update command and correct problems by editing data in the Excel spreadsheet or static input files.

The fastest way to troubleshoot the yaml (once it is produced) is to run the [Swagger command line validator](https://www.npmjs.com/package/swagger-cli). The validator stops at the first error encountered, so rerun the command until it executes cleanly. Note that the error messages are not ideal, so some research may be required to resolve each one.

## Generating Code

Once the swagger file (TOBSwagger.yaml) has been generated and validated, generate the code from the swagger file. The generated code will be checked in and is useful for comparison with previous versions of the generated code, but is not used directly in the application. A developer needs to manually determine the impact of the changes to the swagger specification and the generated code and based on that, update the code in the app.

To generated the code:

1. Remove the "gen" directory (e.g. rm -rf gen)
2. Run the script "extcodegen.sh" or "extcodegen.bat" from a command line

The script is configured to invoke the code generator with a consistent and correct set of command line parameters for the project.

## Developer Workflow: API Evolution

Please review the Developer Workflow sections of the [Swagger-Codegen-Extension](https://github.com/bcgov/Swagger-Codegen-Extension):

For this project, run the extcodegen.bat/extcodegen.sh scripts with no arguments to generate code into the gen/ folder.  Run the .sh script with --help to see the default settings and command line overrides that are possible. Review the .bat script to see the same information.  

The set up for this app is:

- generate django
- use the swagger-codegen-config.json config file
- use the jar files in the repo
- generate all
- output the code to the gen/ directory

## Committing Changes

Before committing changes, make sure that you:

* Exit out of Excel, so the backup file is not committed.
* Verify the swagger changes are what you expect (e.g. with a visual diff tool)
* Validate the swagger file using the swagger-cli.
* Generate the code from the latest version of the swagger file
  * Be sure to delete the old generated code and regen, to remove files related to tables removed from the swagger.

A .gitignore file has been setup to ensure that only needed files go into the repo.  Make sure when committing that you don't accidentally put temporary working files into the repo.

## Tips for Applying the API Changes to the Application

### Before Starting

- Verify the application builds cleanly and the tests execute before beginning.
- Review the TOBSwagger.yaml file changes (git diff with previous version) to see what changes have been made. Review the related JIRA ticket for why the changes have been made.

### Generate and Apply Automatic Changes

- Generate the code using the extcodegen.bat/extcodegen.sh script
- Copy the "as is" code to the appropriate place in the project
- Diff the "manually maintained" code to see what new files have been created, or files have been removed.
- Make the corresponding changes to the application code  - add/remove application files.

### Compile, Test and Fix ###

- Attempt to compile the app, and find/correct the errors.
  - For each error, trace back from the code to the point in the API that was changed to trigger the error. For example, eaach Services.Impl file corresponds to a path in the Swagger definition, and each path contains references to specific Models/ViewModels in the definition. If a Services.Impl file has an error, chances are it is related to changes in those areas of the API.
  - Use the information issue tracking (e.g. trello or github issues) to understand why the API changed in that area.
  - Fix the error.
- Run the test suite and find/correct and test failures.

### Review the Test Data and correct

The TestData/ directory contains the test data for the app. IF any changes were made to the app that might afffect the test data (data table, column names changed), adjust the corresponding test data in the Excel file and regenerate and load the data.

Once correct, attempt to load the data per the instructions in that folder. If the API scripts load the data, consider dropping and recreating the database, and loading fresh test data.

## Check Constraints

Check constraints are not supported by the following:

- Excel spreadsheet
- YAML format Swagger/OpenAPI specification
- Code generated from the Swagger/OpenAPI specification
- Entity Framework/Django

As such, if there is a special requirement to have a check constraint, they can only be added through a custom database migration at the Framework level.  This is a manual process done by a software developer.

Note that a check constraint added in this manner is unknown to Entity Framework/Django, and so if any changes are made by Entity Framework/Django to a model object containing such a constraint, it is possible automatically generated migrations involving changes to that object will fail.

Migrations that do not involve any changes to an object containing constraints or other hand made additions would not be affected.  

The best practice with any migration is to test before deployment, and only deploy if the migration is successful in the test environment.
