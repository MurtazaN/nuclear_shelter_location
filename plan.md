|Phase|Timeline|Key Deliverables|Course Milestone
|---|---|---|---
|1. Setup & Data|Now - Feb 20|• Set up repo & env<br>• Script to fetch Census/Zip data<br>• Script to fetch Urban Target coordinates|Project Proposal (Submitted)
|2. Lit Review|Feb 21 - Feb 26|• Summarize Kratica et al. (2001)<br>• Explain how GA applies to UFLP<br>• Submit 1-2 page review|Literature Review (Due Feb 26)
|3. Baseline & GA Core|Feb 27 - Mar 10|• Implement Greedy Heuristic (Baseline)<br>"• Implement GA (Selection, Crossover, Mutation)"<br>"• Implement Fitness Function (Coverage, Safety, Access)"|Progress Report 1 (Due Mar 12)
|4. Optimization & Eval|Mar 13 - Mar 28|• Tune GA hyperparameters<br>• Run comparisons (GA vs. Greedy)<br>• Generate visualizations (maps)|Progress Report 2 (Due Mar 30)
|5. Paper & Polish|Mar 31 - Apr 13|"• Write full paper (Intro, Methods, Results, Conclusion)"<br>• Clean code & comments<br>• Final submission|Final Submission (Due Apr 13) 

---

1. Diagnose current failure mode.
2. Improve GA search mechanics without changing fitness terms.
3. Retune and validate against greedy with stronger protocol.

Your current results show classic premature convergence plus a very strong greedy baseline.

- Greedy is doing exact marginal uncovered-population gain each step in baseline_greedy.py, so it is hard to beat with a generic GA.
- The budget is matched fairly through GA shelter count in main.py and main.py, and both methods have identical cost ratio in final_results.json and final_results.json.
- GA fitness plateaus very early: best value reached by gen 28 in convergence_data.csv and unchanged at gen 219 in convergence_data.csv.
- Optuna picked a small/high-pressure regime: pop_size 40, tournament 5, adaptive mutation off in final_results.json, final_results.json, final_results.json.

How to make GA stronger than greedy, without adding new metrics:

1. Use fixed-budget encoding (most important)
- Your objective is effectively a fixed-$K$ selection when you compare with equal shelters.
- Keep exactly $K$ ones in each chromosome, instead of free bit flips.
- Replace current mutation in genetic_algo.py with swap mutation (flip one 1 to 0 and one 0 to 1).
- Add child repair after crossover in genetic_algo.py so each child stays at exactly $K$.

2. Seed GA with greedy, then optimize beyond it
- Initialize part of population with greedy solution + perturbed greedy variants, instead of only Bernoulli init in genetic_algo.py.
- This gives GA a strong starting point and lets it search swap improvements greedy misses.

3. Add local search to elites (memetic GA)
- After each generation, run a small 1-swap or 2-swap hill-climb on top elites.
- Greedy is one-step myopic; local swap search can undo earlier choices and exceed greedy while keeping same fitness definition.

4. Reduce selection pressure, increase diversity
- Tournament size 5 with pop 40 is aggressive and can collapse diversity fast from final_results.json and final_results.json.
- Try tournament size 2-3, elitism 1-2, and inject random immigrants each generation.
- This targets the early plateau seen in convergence_data.csv.

5. Turn adaptive mutation back on and make it plateau-responsive
- Adaptive mutation is currently off in final_results.json, while logic exists in genetic_algo.py.
- Keep it on, shorten stagnation window, and trigger stronger perturbation on no-improvement streaks.

6. Tune hyperparameters across multiple seeds, not one seed per trial
- Current Optuna trial uses one seed in optuna_tuning.py.
- For each trial, evaluate 3-5 seeds and optimize mean or median fitness.
- This prevents picking brittle settings that look good on one random run.

7. Spend compute budget on breadth, not long flat tails
- You plateau by ~30 generations, yet run 220.
- Prefer larger population + fewer generations with restart-on-stagnation.
- This usually outperforms long runs in one converged basin.

Implemented :
1. Fixed-$K$ chromosomes with swap mutation + repair.
2. Greedy-seeded population + elite local search.
3. Multi-seed Optuna objective with lower selection pressure.