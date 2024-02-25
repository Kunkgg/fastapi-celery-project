
## 启动低优先级队列 worker

```
docker-compose run --rm celery_worker celery -A main.celery worker  -l info -Q low_priority
```