
while true; do
  echo "Re-starting Django runserver"
  DJANGO_ENV=local poetry run python manage.py runsslserver 0.0.0.0:8000
  sleep 1
done
