(f (max prev curr)' (
    (curr print)
    ((((curr prev +) max >) curr)'
     ((curr 0 =) (max 0 1 f))'
     ((max curr (curr prev +) f))'
     if)
)' defun)

(345 0 0 f)