MODULE = cluedo

run:
	@py -m $(MODULE)

test:
	@pytest

logclear:
	@cd logs/pytest
	for %F in (*) do if %~zF equ 0 del "%F"