// frontend/pages/problem/[id].js
import { useRouter } from "next/router";
import useSWR from "swr";
import { useState } from "react";

const fetcher = (url) => fetch(url).then(r => r.json());

export default function Problem() {
  const router = useRouter();
  const { id } = router.query;
  const { data, error } = useSWR(id ? `http://localhost:8000/problems/${id}` : null, fetcher);
  const [selected, setSelected] = useState(null);
  const [steps, setSteps] = useState("");

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  const submit = async () => {
    const resp = await fetch("http://localhost:8000/submissions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problem_id: data.id,
        user: "sujal",
        selected_index: selected,
        steps,
        time_taken_seconds: 30
      })
    });
    const result = await resp.json();
    alert(result.correct ? "Correct ✅" : "Wrong ❌");
  };

  return (
    <div style={{ padding: 24 }}>
      <button onClick={() => router.back()}>← Back</button>
      <h1>{data.subject} — {data.topic} ({data.difficulty})</h1>
      <p>{data.stem}</p>
      <div>
        {data.options.map((opt, i) => (
          <div key={i} style={{ margin: 8 }}>
            <label>
              <input type="radio" name="opt" value={i} onChange={() => setSelected(i)} />
              {" "}{opt}
            </label>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12 }}>
        <h4>Show your steps</h4>
        <textarea value={steps} onChange={(e)=>setSteps(e.target.value)} rows={6} cols={60} />
      </div>

      <div style={{ marginTop: 12 }}>
        <button onClick={submit} disabled={selected === null}>Submit</button>
      </div>

      <div style={{ marginTop: 20 }}>
        <h4>Explanation</h4>
        <p>{data.explanation}</p>
      </div>
    </div>
  )
}
