from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
SIGMA=5.670374419e-8

def rho(h): return 1.225*math.exp(-max(h,0)/8500)

def simulate(duration:float,dt:float=0.05,nose_radius:float=0.6,bc:float=500):
    h=70000.0; v=2600.0; gamma=math.radians(-7); temp=300.0; rows=[]; heat_load=0.0
    for i in range(int(duration/dt)+1):
        t=i*dt; d=rho(h); qdyn=.5*d*v*v; drag=qdyn/bc
        heat=1.5e-4*math.sqrt(max(d,0)/nose_radius)*v**3
        rad=.85*SIGMA*(temp**4-290**4); net=max(-50000,heat-rad); temp += net/2.2e6*dt; heat_load += max(heat,0)*dt
        rows.append({"t_s":t,"altitude_m":h,"speed_mps":v,"density_kg_m3":d,"dynamic_pressure_pa":qdyn,"heat_flux_proxy_w_m2":heat,"surface_temp_k":temp,"heat_load_j_m2":heat_load})
        if h<=0 or v<=100: break
        h += v*math.sin(gamma)*dt; v=max(0,v+(-drag-9.80665*math.sin(gamma))*dt)
        gamma += -(9.80665/max(v,1))*math.cos(gamma)*dt
    return rows

def metrics(rows):
    return {"samples":len(rows),"peak_heat_flux_proxy_w_m2":round(max(r["heat_flux_proxy_w_m2"] for r in rows),2),"peak_surface_temp_k":round(max(r["surface_temp_k"] for r in rows),2),"total_heat_load_j_m2":round(rows[-1]["heat_load_j_m2"],2)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--duration",type=float,default=80); p.add_argument("--output",type=Path,default=Path("artifacts")); a=p.parse_args()
    rows=simulate(a.duration); a.output.mkdir(parents=True,exist_ok=True)
    with (a.output/"thermal_history.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    report=metrics(rows); (a.output/"summary.json").write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
