FOO ?= 83

new_prep_for_development:
	python txlege84/manage.py bootstrapchamber
	python txlege84/manage.py bootstrapparty
	python txlege84/manage.py bootstrapsubject
	python txlege84/manage.py bootstraplegislator

prep_for_development:
	python txlege84/manage.py downloadopenstatesdata
	python txlege84/manage.py bulkloadlegislators
	python txlege84/manage.py bulkloadcommittees
	python txlege84/manage.py bulkloadbills -s $(FOO)
	python txlege84/manage.py bootstraptopics
	python txlege84/manage.py loadfakeissues
	python txlege84/manage.py loadfakeexplainers
