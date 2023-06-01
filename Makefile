

run:
	kubectl apply -f ./kubernetes/flaskapp.yaml
	kubectl apply -f ./kubernetes/mongo-svc.yaml
	kubectl apply -f ./kubernetes/mongo.yaml
	kubectl apply -f ./kubernetes/mongo-pv.yaml

build:
	docker build -t meteorological-center-web:latest .
	docker build -f crawling/Dockerfile.water -t meteorological-center-crawling-water:latest crawling
	docker build -f crawling/Dockerfile.elec -t meteorological-center-crawling-elec:latest crawling

clean:
	kubectl delete -f ./kubernetes/flaskapp.yaml
	kubectl delete -f ./kubernetes/mongo-svc.yaml
	kubectl delete -f ./kubernetes/mongo.yaml
	kubectl delete -f ./kubernetes/mongo-pv.yaml
