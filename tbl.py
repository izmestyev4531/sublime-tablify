import sublime
import sublime_plugin
import re

class TblCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selected_region in self.view.sel():
            text = self.view.substr(selected_region)
            lengths = []
            lines = text.split("\n")
            all_tokens = []
            for line in lines:
                tokens = re.findall("(?:^|,)\s*\"?((?<=(?<!\")\")(?:[^\"]*|(?:[^\"]*\"[^\"]*\"[^\"]*)+?)(?=\"(?!\"))|[^,]*)\"?(?=\s*,|\s*$)", line)
                while tokens[-1]=="": 
                    tokens.pop() 
                all_tokens.append(tokens)
                tokens_count = len(tokens)
                len_lengths = len(lengths)
                for col in range(0, tokens_count):
                    len_token = max(1, len(tokens[col]))
                    if col >= len_lengths:
                        lengths.append(len_token)
                    else:
                        lengths[col] = max(len_token, lengths[col])
            lines_count = len(lines)
            table = ""
            for l in range(0, lines_count):
                last_line_case = l == lines_count - 1 
                tokens = all_tokens[l]
                tokens_count = len(tokens)
                columns_count = len(lengths)
                if l == 0:
                    for c in range(0, columns_count):
                        if c == 0:
                            table += "╔"
                        for t in range(0, lengths[c]):
                            table += "═"
                        if c < columns_count - 1:
                            table += "╦"
                        else:
                            table += "╗"
                for c in range(0, columns_count):
                    cell = tokens[c] if c < tokens_count else "" 
                    if c == 0:
                        table += "\n║"
                    table += cell.ljust(lengths[c], " ")
                    table += "║"
                for c in range(0, columns_count):
                    if c == 0:
                        if last_line_case:
                            table += "\n╚"
                        else:
                            table += "\n╠"
                    for s in range(0, lengths[c]):
                        table += "═"
                    last_column_case = c == columns_count - 1
                    if last_line_case:
                        if last_column_case:
                            table += "╝"
                        else:
                            table += "╩"
                    else:
                        if last_column_case:
                            table += "╣"
                        else:
                            table += "╬"
            self.view.replace(edit, selected_region, table)

class DetblCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selected_region in self.view.sel():
            text = self.view.substr(selected_region)
            lengths = []
            lines = text.split("\n")
            all_tokens = []
            new_text = ""
            for line in lines:
                tokens = re.findall("(?<=║)[^║]+", line)
                if len(tokens) > 0:
                    if new_text!="":
                        new_text += "\n"
                    new_tokens = list(map(lambda t: t.strip() if t.find(',') == -1 else "\"" + t.strip() + "\"", tokens))
                    while new_tokens[-1]=="": 
                        new_tokens.pop() 
                    new_text += ",".join(new_tokens)   
            self.view.replace(edit, selected_region, new_text)