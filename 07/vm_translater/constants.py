C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

# pointerセグメントはRAMの3~4番目(THIS, THAH)
# にマッピングされる
TEMP_BASE_ADDRESS = 5
# tempセグメントはRAMの5~12番目(R5...R12)
POINTER_BASE_ADDRESS = 3
