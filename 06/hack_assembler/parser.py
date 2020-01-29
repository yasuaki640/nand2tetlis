import re  # 正規表現操作モジュールをインポート

# 各アセンブリコマンドをフィールドトシンボルに分解する

# コマンドタイプを定数として定義
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

# 同じパターンで何度も検索するので事前に検索するパターンをコンパイルする
A_COMMAND_PATTERN = re.compile(r'@([0-9a-zA-Z_\.\$:]+)')
L_COMMAND_PATTERN = re.compile(r'\(([0-9a-zA-Z_\.\$:]*)\)')
C_COMMAND_PATTERN = re.compile(r'(?:(A?M?D?)=)?([^;]+)(?:;(.+))?')


class HackParser():
    # コンストラクタを定義
    # 入力ファイルを開きパースを行う準備をする
    def __init__(self, filepath):
        self.current_command = None
        self.f_hack = open(filepath)

    # with構文で必要、withブロック前後の処理を記述する
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f_hack.close()

    # 入力から次のコマンドを読み、それを現在のコマンドにする。
    def advance(self):
        while True:
            line = self.f_hack.readline()
            if not line:
                self.current_command = None
                break

            # 空白を除去
            line_trimmed = line.strip().replace(' ', '')
            # コメントは無視する
            comment_i = line_trimmed.find('//')
            # 空白でもコメントでもない場合は
            # current_comandに読み込んだコマンドを突っ込む
            if comment_i != -1:
                line_trimmed = line_trimmed[:comment_i]

            if line_trimmed != '':
                self.current_command = line_trimmed
                break

        return self.current_command

    # 現コマンドの種類を返す。
    def command_type(self):
        # Aコマンドは@Xxxの型式
        if self.current_command[0] == '@':
            return A_COMMAND
        # Lコマンドは疑似コマンド、(Xxx)の型式
        elif self.current_command[0] == '(':
            return L_COMMAND
        else:
            return C_COMMAND

    # 現コマンド@Xxxまたは疑似コマンド(Xxx)のXxxを返す
    # Xxxはシンボルまたは10進数の数値
    def symbol(self):
        cmd_type = self.command_type()
        if cmd_type == A_COMMAND:
            m = A_COMMAND_PATTERN.match(self.current_command)
            # コマンド種類がAコマンドとなっているのに
            # Aコマンドのパターンに一致しなかったら
            if not m:
                # メッセージでエラーを返す
                raise Exception('Parsing symbol failed')
            # マッチした文字列を返す
            return m.group(1)

        elif cmd_type == L_COMMAND:
            m = L_COMMAND_PATTERN.match(self.current_command)
            if not m:
                raise Exception('Parsing symbol failed')
            return m.group(1)
        else:
            raise Exception('Cunrrent command is not A_COMMAND or L_COMMAND')

    # 現在のC命令のdestニーモニックを返す
    def dest(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.current_command)
            return m.group(2)
        else:
            raise Exception('Current command is not C_COMMAND')

    # 現C命令のcompニーモニックを返す
    def comp(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.current_command)
            return m.group(2)
        else:
            raise Exception('Cunrrent command is not C_COMMAND')
        
    # 現C命令のjumpニーモニックを返す
    def jump(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.current_command)
            return m.group(3)
        else:
            raise Exception('Cunrrent command is not C_COMMAND')
