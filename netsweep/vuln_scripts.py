import importlib

class VulnRunner:
    def run(self, target, script_name):
        try:
            module = importlib.import_module(f"netsweep.scripts.{script_name}")
            result = module.check(target)
            return {"target": target, "script": script_name, "vulnerable": result}
        except Exception as e:
            return {"error": str(e)}
