

run:
	kubectl apply -f ./kubernetes/flaskapp.yaml
	kubectl apply -f ./kubernetes/mongo-pv.yaml
	kubectl apply -f ./kubernetes/mongo.yaml
	kubectl apply -f ./kubernetes/mongo-svc.yaml

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
