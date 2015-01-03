prep_for_development:
	python txlege84/manage.py downloadopenstatesdata
	python txlege84/manage.py bulkloadlegislators
	python txlege84/manage.py bulkloadcommittees
	python txlege84/manage.py bulkloadbills -s 83
	python txlege84/manage.py updatebills --bulk
	python txlege84/manage.py bootstraptopics
	python txlege84/manage.py loadfakeissues
