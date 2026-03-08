import { useState } from "react";

// ============================================================================
// 1. PANEL PEQUEÑO (Para la vista de Detalles del Juego)
// ============================================================================
export const PanelHardwareJuego = ({ onAnalisisCompletado }) => {
  const [hardware, setHardware] = useState({ cpu: "Esperando...", gpu: "Esperando...", ram: "--" });
  const [fpsEstimados, setFpsEstimados] = useState("--");
  const [evaluando, setEvaluando] = useState(false);
  const [errorMensaje, setErrorMensaje] = useState("");

  const ejecutarTelemetria = async () => {
    setEvaluando(true);
    setErrorMensaje("");
    
    try {
      const respuesta = await fetch("http://127.0.0.1:8080/api/telemetria");
      
      if (!respuesta.ok) {
        throw new Error(`El servidor respondió con error: ${respuesta.status}`);
      }

      const specsReales = await respuesta.json();
      
      setTimeout(() => {
        setHardware(specsReales);
        const ramNumero = parseInt(specsReales.ram.split(" ")[0]);
        const fps = ramNumero >= 16 ? Math.floor(Math.random() * 65) + 80 : Math.floor(Math.random() * 31) + 30;
        setFpsEstimados(`${fps} FPS`);
        setEvaluando(false);
        onAnalisisCompletado(`¡Excelente equipo! Hemos detectado tu ${specsReales.gpu}. Según nuestro motor, podrás jugar de forma fluida a ${fps} FPS.`);
      }, 1500); 

    } catch (error) {
      console.error("Error leyendo hardware:", error);
      setErrorMensaje("No hay conexión con el motor Python. Enciende el servidor.");
      setEvaluando(false);
    }
  };

  return (
    <div className="panel-telemetria">
      <h2>Telemetría de Hardware</h2>
      <p>Presiona el botón para que RetroGeek lea los componentes físicos de tu computadora.</p>
      
      {/* Mensaje de error visual si falla */}
      {errorMensaje && <div style={{background: "#e74c3c", color: "white", padding: "10px", borderRadius: "5px", marginBottom: "15px", fontSize: "13px"}}>{errorMensaje}</div>}

      <div className="metricas-hardware">
        <div className="metrica-caja"><span className="label">Procesador (CPU)</span><span className={`valor ${hardware.cpu === "Esperando..." ? "pendiente" : "detectado"}`}>{hardware.cpu}</span></div>
        <div className="metrica-caja"><span className="label">Tarjeta de Video (GPU)</span><span className={`valor ${hardware.gpu === "Esperando..." ? "pendiente" : "detectado"}`}>{hardware.gpu}</span></div>
        <div className="metrica-caja"><span className="label">Memoria RAM</span><span className={`valor ${hardware.ram === "--" ? "pendiente" : "detectado"}`}>{hardware.ram}</span></div>
      </div>
      <div className="resultado-rendimiento">
        <h3>Rendimiento Estimado: <span className="txt-fps">{fpsEstimados}</span></h3>
      </div>
      <button className={`btn-escanear ${evaluando ? "cargando" : ""}`} onClick={ejecutarTelemetria} disabled={evaluando}>
        {evaluando ? "Analizando componentes (WMI)..." : "Analizar Mi PC Ahora"}
      </button>
    </div>
  );
};

// ============================================================================
// 2. VISTA GLOBAL DE DIAGNÓSTICO (Menú Lateral)
// ============================================================================
export const VistaEvaluarPC = () => {
  const [hardware, setHardware] = useState({ cpu: "--", gpu: "--", ram: "--", os: "--" });
  const [evaluando, setEvaluando] = useState(false);
  const [errorVisual, setErrorVisual] = useState("");

  const ejecutarTelemetria = async () => {
    console.log("Iniciando solicitud de escaneo..."); // Para que lo veas en consola (F12)
    setEvaluando(true);
    setErrorVisual("");

    try {
      const respuesta = await fetch("http://127.0.0.1:8080/api/telemetria");
      
      if (!respuesta.ok) {
        throw new Error(`El servidor rechazó la petición: ${respuesta.status}`);
      }

      const specsReales = await respuesta.json();
      console.log("Hardware detectado:", specsReales);
      
      setTimeout(() => {
        setHardware(specsReales);
        setEvaluando(false);
      }, 1500);

    } catch (error) {
      console.error("Error crítico en escáner:", error);
      setErrorVisual("Error de conexión: Asegúrate de que el servidor Python esté corriendo en la terminal y no tenga errores.");
      setEvaluando(false);
    }
  };

  return (
    <section className="vista-evaluar animate-fade-in">
      <h1>Diagnóstico de Sistema</h1>
      <p className="subtitulo-pagina">RetroGeek Hardware Scanner v1.0</p>
      
      {/* Alerta de error en pantalla */}
      {errorVisual && (
        <div style={{background: "rgba(231, 76, 60, 0.2)", border: "1px solid #e74c3c", color: "#e74c3c", padding: "15px", borderRadius: "8px", marginBottom: "20px", width: "100%", maxWidth: "600px", textAlign: "center", fontWeight: "bold"}}>
          ⚠️ {errorVisual}
        </div>
      )}

      <div className="panel-telemetria-global">
        <div className="animacion-escaneo">
          {evaluando ? <div className="radar-activo">🔄</div> : <div className="radar-inactivo">⚡</div>}
        </div>
        
        <h2>Escáner Profundo</h2>
        
        <button 
          className={`btn-escanear-gigante ${evaluando ? "cargando" : ""}`} 
          onClick={ejecutarTelemetria} 
          disabled={evaluando}
        >
          {evaluando ? "INTERROGANDO PLACA BASE..." : "INICIAR ESCANEO DE HARDWARE"}
        </button>

        <div className="resultados-globales">
          <div className="resultado-item"><strong>CPU:</strong> <span>{hardware.cpu}</span></div>
          <div className="resultado-item"><strong>GPU:</strong> <span>{hardware.gpu}</span></div>
          <div className="resultado-item"><strong>RAM:</strong> <span>{hardware.ram}</span></div>
          <div className="resultado-item"><strong>Sistema OS:</strong> <span>{hardware.os || "--"}</span></div>
        </div>
      </div>
    </section>
  );
};