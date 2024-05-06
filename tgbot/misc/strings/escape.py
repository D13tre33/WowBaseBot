def escape(s: str) -> str:
    if type(s) is str:
        return s.replace(".", "\\.").replace("-", "\\-").replace("(", "\\(").replace(")", "\\)").replace("{", "\\{") \
            .replace("}", "\\}").replace("!", "\\!").replace("?", "\\?").replace("=", "\\=").replace("_", "\\_") \
            .replace("[", "\\[").replace("]", "\\]").replace("+", "\\+").replace(">", "\\>").replace("<", "\\<")
    return "None"
