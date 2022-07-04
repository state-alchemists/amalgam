echo "${_BOLD}${_YELLOW}Test application${_NORMAL}"
pytest -rP -v --cov="$(pwd)" --cov-report html
echo "${_BOLD}${_YELLOW}Test completed${_NORMAL}"