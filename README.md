# The Survox Python SDK

This package has code for a python SDK for interacting with the Survox API.  The documentation for the API is
currently available as [swagger](https://swagger-ui-dev.survoxinc.com/)

## SKD Overview

We don't have documentation for the SDK yet, but a good example of using the SDK is in demodata/demodata.py, which
uses the SDK to install various example resources onto the local system.

The general pattern of the SDK is illustrated by looking at the quotas endpoints in the API and how they translate
into SDK calls.

    # instantiate an api object
    api = SurvoxAPI('my_host', 'my_apikey')

    # Example of a resource collection endpoint
    # /survoxapi/surveys/my_survey/quotas/ - get, post/create, delete all quotas for my_survey
    quotas = api.surveys('my_survey').quotas.list()  # for a collection GET is done via a list() method
    quotas = api.surveys('my_survey').quotas.create(quotas_to_create)  # for a collection POST is done via a create() method
    api.surveys('my_survey').quotas.delete({'delete': 'delete'})  # for a collection DELETE is done via a delete() method
    api.surveys('my_survey').quotas.reset()  # for a misc. actions, there's a method for performing the action
    api.surveys('my_survey').quotas.history(start=, end=, quotas=)
    

    # Example of a specific resource_endpoint
    # /survoxapi/surveys/my_survey/quotas/my_quota1 - get, put, delete all quotas for my_survey
    quotas = api.surveys('my_survey').quota('my_quota1').get()  # for a resource GET is done via a get() method
    quotas = api.surveys('my_survey').quota('my_quota1').set(new_quota)  # for a resource PUT is done via a set() method
    quotas = api.surveys('my_survey').quota('my_quota1').increment(4) # for a misc. actions, there's a method for performing the action


# History
0.0.2
===
- flush out next round of endpoints

0.0.1
===
- Initial version
