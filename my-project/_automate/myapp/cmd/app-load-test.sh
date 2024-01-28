export PYTHONUNBUFFERED=1
echo "Start load test"
locust {%if input.myapp_load_test_headless %}--headless{% endif %} \
    --web-port {{ input.myapp_load_test_port }} \
    --users {{ input.myapp_load_test_users }} \
    --spawn-rate {{ input.myapp_load_test_spawn_rate }} \
    -H {{ input.myapp_load_test_url }}