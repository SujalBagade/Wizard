// frontend/pages/index.js
import useSWR from "swr";
import Link from "next/link";

const fetcher = (url) => fetch(url).then(r => r.json());

export default function Home() {
  const { data, error } = useSWR("http://localhost:8000/problems", fetcher);

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ padding: 24, fontFamily: "system-ui, sans-serif" }}>
      <h1>Wizard — Problems</h1>
      <p>{data.count} problems</p>
      <div>
        {data.results.map(p => (
          <div key={p.id} style={{ border: "1px solid #ddd", padding: 12, margin: 8 }}>
            <h3>{p.subject} • {p.topic} • {p.difficulty}</h3>
            <p>{p.stem}</p>
            <Link href={`/problem/${p.id}`}><a>Open →</a></Link>
          </div>
        ))}
      </div>
    </div>
  )
}
