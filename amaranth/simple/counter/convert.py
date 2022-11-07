# --- CONVERT ---
from amaranth.back import verilog
from main import UpCounter

top = UpCounter(25)
with open("counter.v", "w") as f:
    f.write(verilog.convert(top, ports=[top.en, top.ovf]))
