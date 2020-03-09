```
<prog> = <stmnts>
<stmts> = <stmnt> ";" <stmnts> // {"var", <ident>, "for", "read", "print", "assert"}
<stmnts> = <epsilon> // {<epsilon>}
<stmnt> = "var" <var_ident> ":" <type> <assign_value> // {"var"}
<stmnt> = <var_ident> ":=" <expr> // {ident}
<stmnt = "for" <var_ident> "in" <expr> ".." <expr> "do" // {"for"}
              <stmnts> "end" "for"
<stmnt> = "read" <var_ident> // {"read}
<stmnt> =  "print" <expr> // {"print"}
<stmnt> "assert" "(" <expr> ")" // {"assert"}
<assign_value> = ":=" <expr>| <epsilon>  // {":="}
<expr> = <opnd> <op> <opnd>
<opnd> = <int> // {int}
<opnd> = <string>  // {string}
<opnd> = <var_ident>  // {ident}
<opnd> = "(" <expr> ")" // {"("}
<type> = "int"  // {"int"}
<type> = "string” // {"string"}
<type> = "bool" // {"bool"}
<var_ident> = <ident>
<reserved_keywords = "var" | "for" | "end" | "in" | "do" | "read" |
                    "print" | "int" | "string" | "bool" | "assert"

```
