# semgrep scan --config rule.yaml --output findings.txt
#
import os

'''
apex,bash,sh,c,cairo,clojure,cpp,csharp,c#,dart,dockerfile,docker,go,java,javascript,js,json,julia,kotlin,lisp,lua,ocaml,php,python,python2,python3,py,r,ruby,rust,scala,scheme,solidity,sol,swift,terraform,hcl,typescript,ts,yaml,xml
'''
# cpp,python,typescript,java,go,c,csharp,java,javascript,rust,bash
def findAllOccurrencesVariable(variable:str):
    os.system("git add .")
    with open("variable_rules.yaml", "w") as f:
        yaml_structure = f"""rules:\n  - id: universal-variable-finder\n    languages: [python,c,cpp,javascript,typescript,java,rust,r,ruby,dockerfile,dart,go]\n    message: Detected {variable} usage\n    pattern: {variable}\n    severity: INFO\n"""
        f.write(yaml_structure)
    # semgrep is required here
    os.system("semgrep scan --config variable_rules.yaml --output findings.txt")


def findAllUsingGrep(variable:str):
    # use grep here
    #
    # first clone then do the stuff
    exclude = "{tmp,bak,txt,json,log,md}"
    os.system(f"grep -rnw --exclude-dir=cache --exclude=*.{exclude} . -e '{variable}' > findings_general.txt")

if __name__ == "__main__":
    findAllOccurrencesVariable("basic_details")
    findAllUsingGrep("basic_details")
