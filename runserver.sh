
while true; do
  echo "Re-starting Django runserver"
  poetry run python manage.py runserver
  sleep 1
done
