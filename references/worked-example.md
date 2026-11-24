# Worked example: both passes

**Original:**
> Great question! Kubernetes liveness probes are a powerful mechanism that enables the kubelet to determine whether a container is healthy — and it's not just a health check, it's your first line of defense. When a probe fails, the container will be automatically restarted by the kubelet, ensuring that your application remains available. However, it's important to note that misconfigured probes could potentially cause cascading restarts, so parameters like `initialDelaySeconds` and `failureThreshold` should be carefully tuned.
>
> Get this right, and your cluster heals itself.

**After Pass 1 (tells removed):** §22 opener, §16 "powerful mechanism", §8 dash, §1 "not just X", §15 "ensuring" rider, §12 "however", §9 "could potentially", §2 closer.
> Kubernetes liveness probes let the kubelet determine whether a container is healthy. When a probe fails, the container will be automatically restarted by the kubelet, which keeps your application available. Misconfigured probes could cause cascading restarts, so parameters like `initialDelaySeconds` and `failureThreshold` should be carefully tuned.

The chatbot is gone, but the text is still heavy: a passive actor, a "will" where nothing is in the future, a heavy "determine whether", and a cause and an instruction in one sentence. "Misconfigured" stays vague because the source does not say which setting is wrong.

**After Pass 2 (STE80 structure):** S6 active voice, S7 simple tense, S1 one idea per sentence, S10 plain words, S14 instruction separate from description.
> A liveness probe tells the kubelet if a container is healthy. If the probe fails, the kubelet restarts the container. This keeps the application available.
>
> Misconfigured probes could cause cascading restarts. You should tune parameters such as `initialDelaySeconds` and `failureThreshold` carefully.

The rewrite keeps the kubelet, the restart, availability, cascading restarts and both parameters. "Could potentially" becomes "could". The tuning advice remains advice. No new failure example is added.
