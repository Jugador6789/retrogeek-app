import { useState, useEffect } from "react";

// ============================================================================
// 1. COMPONENTE DE TELEMETRÍA CON GRÁFICAS VISUALES
// ============================================================================
const PanelTelemetriaGrafica = () => {
  const [hardware, setHardware] = useState(null);
  const [evaluando, setEvaluando] = useState(false);
  const [puntuacion, setPuntuacion] = useState({ cpu: 0, gpu: 0, ram: 0, total: 0 });

  const ejecutarAnalisis = async () => {
    setEvaluando(true);
    try {
      const respuesta = await fetch("http://127.0.0.1:8080/api/telemetria");
      const specs = await respuesta.json();
      
      setTimeout(() => {
        setHardware(specs);
        
        // --- Lógica de Simulación de Rendimiento ---
        const ramNum = parseInt(specs.ram.split(" ")[0]) || 8;
        const ptsRam = ramNum >= 16 ? 100 : (ramNum >= 8 ? 60 : 30);
        
        const isGpuDedicada = specs.gpu.toUpperCase().includes("NVIDIA") || specs.gpu.toUpperCase().includes("AMD");
        const ptsGpu = isGpuDedicada ? 95 : 40;
        
        const ptsCpu = specs.cpu.includes("i9") || specs.cpu.includes("i7") || specs.cpu.includes("Ryzen 7") ? 90 : 65;
        
        const total = Math.round((ptsRam + ptsGpu + ptsCpu) / 3);
        
        setPuntuacion({ cpu: ptsCpu, gpu: ptsGpu, ram: ptsRam, total: total });
        setEvaluando(false);
      }, 1500);
    } catch (error) {
      console.error("Error WMI:", error);
      setEvaluando(false);
    }
  };

  // Pequeño componente interno para dibujar las barras
  const BarraProgreso = ({ label, porcentaje, color }) => (
    <div style={{ marginBottom: "10px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", marginBottom: "4px" }}>
        <span>{label}</span>
        <span>{porcentaje}%</span>
      </div>
      <div style={{ width: "100%", height: "8px", background: "#333", borderRadius: "4px", overflow: "hidden" }}>
        <div style={{ width: `${porcentaje}%`, height: "100%", background: color, transition: "width 1s ease-in-out" }}></div>
      </div>
    </div>
  );

  return (
    <div className="panel-telemetria-avanzado" style={{ background: "#1a1a1a", padding: "20px", borderRadius: "10px", marginTop: "20px" }}>
      <h3 style={{ borderBottom: "1px solid #333", paddingBottom: "10px" }}>⚡ Análisis de Rendimiento</h3>
      
      {!hardware && (
        <p style={{ fontSize: "14px", color: "#aaa" }}>Haz clic en el botón para evaluar si tu PC puede correr este juego con gráficos en Ultra.</p>
      )}

      {hardware && (
        <div style={{ marginTop: "15px" }}>
          <BarraProgreso label={`Procesador (${hardware.cpu.substring(0, 20)}...)`} porcentaje={puntuacion.cpu} color="#3498db" />
          <BarraProgreso label={`Gráficos (${hardware.gpu.substring(0, 20)}...)`} porcentaje={puntuacion.gpu} color="#2ecc71" />
          <BarraProgreso label={`Memoria RAM (${hardware.ram})`} porcentaje={puntuacion.ram} color="#9b59b6" />
          
          <div style={{ textAlign: "center", marginTop: "20px", padding: "10px", background: puntuacion.total > 75 ? "rgba(46, 204, 113, 0.2)" : "rgba(241, 196, 15, 0.2)", borderRadius: "5px" }}>
            <h4 style={{ margin: 0, color: puntuacion.total > 75 ? "#2ecc71" : "#f1c40f" }}>
              Índice de Compatibilidad: {puntuacion.total}%
            </h4>
            <p style={{ margin: "5px 0 0 0", fontSize: "13px" }}>
              {puntuacion.total > 75 ? "¡Tu PC volará con este juego!" : "El juego correrá, pero sugerimos bajar los gráficos a Medio."}
            </p>
          </div>
        </div>
      )}

      <button 
        onClick={ejecutarAnalisis} 
        disabled={evaluando}
        style={{ width: "100%", padding: "12px", marginTop: "20px", background: evaluando ? "#555" : "#0078F2", color: "white", border: "none", borderRadius: "5px", cursor: evaluando ? "wait" : "pointer", fontWeight: "bold" }}
      >
        {evaluando ? "Analizando Componentes..." : "EVALUAR RENDIMIENTO AHORA"}
      </button>
    </div>
  );
};

// ============================================================================
// 2. VISTA PRINCIPAL (Combina Video, Info, Reseñas y Telemetría)
// ============================================================================
export const DetalleAvanzado = ({ juegoId }) => {
  const [juego, setJuego] = useState(null);

  useEffect(() => {
    // Por ahora simulamos que pedimos el ID 1 para ver el resultado
    fetch(`http://127.0.0.1:8080/api/juegos/${juegoId || 1}`)
      .then(res => res.json())
      .then(data => setJuego(data));
  }, [juegoId]);

  if (!juego) return <h2 style={{color: 'white', textAlign: 'center'}}>Cargando bóveda de datos...</h2>;

  return (
    <div style={{ color: "white", maxWidth: "1000px", margin: "0 auto", padding: "20px", animation: "fadeIn 0.5s" }}>
      
      {/* SECCIÓN SUPERIOR: Video y Datos Rápidos */}
      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px" }}>
        
        {/* Lado Izquierdo: Reproductor de Video */}
        <div style={{ background: "#000", borderRadius: "10px", overflow: "hidden", aspectRatio: "16/9" }}>
          {juego.video_url ? (
            <iframe 
              width="100%" 
              height="100%" 
              src={juego.video_url} 
              title="Trailer del Juego" 
              frameBorder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowFullScreen
            ></iframe>
          ) : (
            <img src={juego.imagen} alt="Portada" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          )}
        </div>

        {/* Lado Derecho: Info y Compra */}
        <div style={{ background: "#1a1a1a", padding: "20px", borderRadius: "10px", display: "flex", flexDirection: "column" }}>
          <h1 style={{ margin: "0 0 10px 0" }}>{juego.titulo}</h1>
          <p style={{ color: "#aaa", fontSize: "14px", margin: "0 0 20px 0" }}>Desarrollador: <strong>{juego.estudio || "Desconocido"}</strong></p>
          
          <div style={{ background: "#222", padding: "15px", borderRadius: "8px", marginBottom: "20px" }}>
            <h2 style={{ margin: "0 0 10px 0" }}>${juego.precio}</h2>
            <button style={{ width: "100%", padding: "15px", background: "#2ecc71", color: "white", border: "none", borderRadius: "5px", fontSize: "16px", fontWeight: "bold", cursor: "pointer" }}>
              {juego.comprado ? "JUEGO EN BIBLIOTECA" : "OBTENER AHORA"}
            </button>
          </div>

          <p style={{ fontSize: "14px", lineHeight: "1.6", flexGrow: 1 }}>{juego.descripcion || "Sin descripción disponible."}</p>
        </div>
      </div>

      {/* SECCIÓN INFERIOR: Telemetría y Reseñas */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginTop: "20px" }}>
        
        {/* Modulo de Telemetría Visual */}
        <PanelTelemetriaGrafica />

        {/* Módulo de Reseñas */}
        <div style={{ background: "#1a1a1a", padding: "20px", borderRadius: "10px", marginTop: "20px" }}>
          <h3 style={{ borderBottom: "1px solid #333", paddingBottom: "10px" }}>⭐ Reseñas de Jugadores</h3>
          
          {juego.resenas && juego.resenas.length > 0 ? (
            <div style={{ maxHeight: "300px", overflowY: "auto", paddingRight: "10px" }}>
              {juego.resenas.map((resena, idx) => (
                <div key={idx} style={{ background: "#222", padding: "15px", borderRadius: "8px", marginBottom: "10px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px" }}>
                    <strong style={{ color: "#3498db" }}>{resena.usuario}</strong>
                    <span style={{ color: "#f1c40f" }}>{"★".repeat(resena.calificacion)}{"☆".repeat(5 - resena.calificacion)}</span>
                  </div>
                  <p style={{ margin: 0, fontSize: "14px", color: "#ddd" }}>"{resena.comentario}"</p>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: "#aaa" }}>Aún no hay reseñas para este juego.</p>
          )}
        </div>
      </div>

    </div>
  );
};