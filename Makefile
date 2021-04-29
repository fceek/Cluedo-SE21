MODULE = cluedo

run-gui:
	@py -m $(MODULE)

run-cmd:
	@cd dev
	py cluedo_dev.py

test:
	@pytest

logclear:
	@cd logs/pytest
	for %F in (*) do if %~zF equ 0 del "%F"