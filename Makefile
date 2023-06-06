

run:
	kubectl apply -f ./kubernetes/flaskapp.yaml
	kubectl apply -f ./kubernetes/mongo-pv.yaml
	kubectl apply -f ./kubernetes/mongo.yaml
	kubectl apply -f ./kubernetes/mongo-svc.yaml
	kubectl apply -f ./kubernetes/flaskapp-svc.yaml

add-cronjob:
	kubectl apply -f ./kubernetes/cronjob.yaml

delete-cronjob:
	kubectl delete -f ./kubernetes/cronjob.yaml

build:
	docker build -t meteorological-center-web:latest .
	docker build -f Dockerfile.crawling -t yuko29/crawling:v1 . 

clean:
	kubectl delete -f ./kubernetes/flaskapp.yaml
	kubectl delete -f ./kubernetes/mongo-svc.yaml
	kubectl delete -f ./kubernetes/mongo.yaml
	kubectl delete -f ./kubernetes/mongo-pv.yaml
	kubectl delete -f ./kubernetes/flaskapp-svc.yaml

setup:
	# kubernetes dashboard
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
	# Create Service Account
	kubectl apply -f ./kubernetes/dashboard-adminuser.yaml

get-token:
	kubectl -n kubernetes-dashboard create token admin-user

