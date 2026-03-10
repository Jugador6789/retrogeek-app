import { useState, useEffect, useRef } from "react";
import "./App.css";
import logoImg from "./assets/logo.png";

// Importamos los componentes externos de Hardware
import { PanelHardwareJuego, VistaEvaluarPC } from "./Telemetria";
// NUEVA IMPORTACIÓN: Traemos el componente avanzado que acabamos de crear
import { DetalleAvanzado } from "./DetalleAvanzado"; 

const NOTICIAS_DB = [
  { id: 1, titulo: "Grand Theft Auto VI rompe récords históricos de preventa", fecha: "5 de Marzo, 2026", img: "https://images.unsplash.com/photo-1605901309584-818e25960b8f?q=80&w=800", extracto: "Rockstar Games confirma que la anticipación ha superado cualquier lanzamiento previo." },
  { id: 2, titulo: "Nintendo anuncia su nueva consola portátil 4K", fecha: "28 de Febrero, 2026", img: "https://images.unsplash.com/photo-1486401899868-0e435ed85128?q=80&w=800", extracto: "La sucesora de la Switch soportará 4K mediante DLSS y todos los cartuchos anteriores." },
  { id: 3, titulo: "Bloodborne llegará a PC este mismo año", fecha: "15 de Febrero, 2026", img: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=800", extracto: "Hidetaka Miyazaki dejó la puerta abierta a un port muy esperado por la PC Master Race." }
];

// ============================================================================
// COMPONENTE 1: TARJETA DE JUEGO
// ============================================================================
const TarjetaJuego = ({ juego, enBiblioteca, estadoInstalacion, progreso, onInstalar, onClick, vista = "grid", esFavorito, onToggleFavorito }) => {
  const esDueño = enBiblioteca || juego.comprado;
  
  return (
    <div className={`tarjeta-juego ${vista === "lista" ? "vista-lista" : ""}`}>
      <div className="contenedor-img" onClick={() => onClick(juego)}>
        <img src={juego.imagen_url} alt={juego.titulo} className="img-juego" />
      </div>
      
      <div className="info-tarjeta">
        <div className="info-header">
          <span className="tag">{juego.tag}</span>
          {enBiblioteca && (
            <button className="btn-favorito" onClick={(e) => { e.stopPropagation(); onToggleFavorito(juego.id); }}>
              {esFavorito ? "❤️" : "🤍"}
            </button>
          )}
        </div>
        
        <h3 onClick={() => onClick(juego)}>{juego.titulo}</h3>
        
        {vista === "lista" && (
          <p className="texto-desarrollador">Desarrollado por: {juego.desarrollador}</p>
        )}
        
        {esDueño ? (
          <div className="area-instalacion">
            {estadoInstalacion === "pendiente" && (
              <button className="btn-instalar" onClick={(e) => { e.stopPropagation(); onInstalar(juego.id); }}>
                <span className="texto-original">En Biblioteca</span>
                <span className="texto-hover">📥 Instalar</span>
              </button>
            )}
            {estadoInstalacion === "descargando" && (
              <div className="barra-descarga-mini">
                <div className="progreso-mini" style={{width: `${progreso}%`}}></div>
                <span className="porcentaje-mini">{progreso}%</span>
              </div>
            )}
            {estadoInstalacion === "instalado" && (
              <button className="btn-jugar">▶ Jugar</button>
            )}
          </div>
        ) : (
          <p className="precio">{juego.precio === 0 ? "Gratis" : `$${juego.precio.toFixed(2)}`}</p>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// COMPONENTE 2: FILA DE JUEGOS CON CARRUSEL MANUAL
// ============================================================================
const FilaJuegos = ({ titulo, juegos, onVerMas, propsTarjeta }) => {
  const scrollRef = useRef(null);

  const scroll = (desplazamiento) => { 
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: desplazamiento, behavior: 'smooth' }); 
    }
  };

  if (!juegos || juegos.length === 0) return null; 

  return (
    <div className="seccion-fila">
      <div className="titulo-fila">
        <h2>{titulo}</h2>
        <span className="ver-mas" onClick={() => onVerMas(titulo, juegos)}>Ver más</span>
      </div>
      <div className="carrusel-envoltorio">
        <button className="btn-carrusel-nav izq" onClick={() => scroll(-800)}>&#10094;</button>
        <div className="scroll-horizontal" ref={scrollRef}>
          {juegos.map((juego) => (
            <TarjetaJuego 
              key={juego.id} 
              juego={juego} 
              estadoInstalacion={propsTarjeta.obtenerEstadoInst(juego.id)} 
              progreso={propsTarjeta.progresoDescarga[juego.id]} 
              onInstalar={propsTarjeta.iniciarInstalacion} 
              onClick={propsTarjeta.irADetalle} 
            />
          ))}
        </div>
        <button className="btn-carrusel-nav der" onClick={() => scroll(800)}>&#10095;</button>
      </div>
    </div>
  );
};

// ============================================================================
// APLICACIÓN PRINCIPAL
// ============================================================================
function App() {
  const [vistaActiva, setVistaActiva] = useState("inicio");
  const [juegoSeleccionado, setJuegoSeleccionado] = useState(null);
  const [categoriaActual, setCategoriaActual] = useState({ titulo: "", juegos: [] });
  
  const [juegosLista, setJuegosLista] = useState([]);
  const [bibliotecaUsuario, setBibliotecaUsuario] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [indiceBanner, setIndiceBanner] = useState(0);

  const [textoBusqueda, setTextoBusqueda] = useState("");
  const [filtroTag, setFiltroTag] = useState("Todos");
  const [filtroPrecio, setFiltroPrecio] = useState("Todos");
  
  const [busquedaBiblioteca, setBusquedaBiblioteca] = useState("");
  const [pestanaBiblioteca, setPestanaBiblioteca] = useState("todos");
  const [vistaBiblioteca, setVistaBiblioteca] = useState("grid");
  const [favoritosIds, setFavoritosIds] = useState([]);
  const [filtroGeneroBiblio, setFiltroGeneroBiblio] = useState("Todos");
  const [filtroCaracteristica, setFiltroCaracteristica] = useState("Todas");
  const [filtroPlataforma, setFiltroPlataforma] = useState("Todas");

  const [progresoDescarga, setProgresoDescarga] = useState({});
  const [juegosDescargando, setJuegosDescargando] = useState([]);
  
  const [chatAbierto, setChatAbierto] = useState(false);
  const [mensajeIA, setMensajeIA] = useState("Asistente listo.");

  // Asignamos características simuladas para probar los filtros
  const enriquecerJuego = (j) => {
    const isMulti = ["Multijugador", "Shooter", "Estrategia"].includes(j.tag);
    return { 
      ...j, 
      plataformas: ["Windows", j.id % 4 === 0 ? "macOS" : null].filter(Boolean), 
      caracteristicas: [
        "Logros", 
        "Partidas guardadas en la nube", 
        isMulti ? "Online Multiplayer" : "Para un solo jugador", 
        j.id % 2 === 0 ? "Compatible con control" : null
      ].filter(Boolean) 
    };
  };

  const cargarDatos = () => {
    fetch("http://127.0.0.1:8080/api/juegos")
      .then(r => r.json())
      .then(datos => { 
        if (Array.isArray(datos)) setJuegosLista(datos.map(enriquecerJuego)); 
        setCargando(false); 
      })
      .catch(e => { 
        console.error("Error BD Tienda:", e); 
        setCargando(false); 
      });

    fetch("http://127.0.0.1:8080/api/biblioteca")
      .then(r => r.json())
      .then(datos => { 
        if (Array.isArray(datos)) setBibliotecaUsuario(datos.map(enriquecerJuego)); 
        else setBibliotecaUsuario([]); 
      })
      .catch(e => console.error("Error BD Biblioteca:", e));
  };

  useEffect(() => { 
    cargarDatos(); 
  }, []);

  const aplicarVista = (nuevaVista, datos) => { 
    setVistaActiva(nuevaVista); 
    if (nuevaVista === 'detalle') setJuegoSeleccionado(datos); 
    if (nuevaVista === 'categoria') setCategoriaActual(datos); 
  };

  const cambiarVista = (nuevaVista, datos = null) => { 
    window.history.pushState({ vista: nuevaVista, datos }, "", ""); 
    aplicarVista(nuevaVista, datos); 
    window.scrollTo(0, 0); 
  };
  
  useEffect(() => {
    window.history.replaceState({ vista: "inicio", datos: null }, "", "");
    const handlePopState = (e) => {
      e.state ? aplicarVista(e.state.vista, e.state.datos) : aplicarVista("inicio", null);
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const iniciarInstalacion = (juegoId) => {
    if (juegosDescargando.includes(juegoId)) return;
    
    setJuegosDescargando(prev => [...prev, juegoId]);
    setProgresoDescarga(prev => ({...prev, [juegoId]: 0}));
    
    const intervalo = setInterval(() => {
      setProgresoDescarga(prev => {
        const nuevoProgreso = (prev[juegoId] || 0) + Math.floor(Math.random() * 8) + 2;
        if (nuevoProgreso >= 100) { 
          clearInterval(intervalo); 
          setJuegosDescargando(activos => activos.filter(id => id !== juegoId)); 
          return {...prev, [juegoId]: 100}; 
        }
        return {...prev, [juegoId]: nuevoProgreso};
      });
    }, 150);
  };

  const obtenerEstadoInst = (juegoId) => {
    if (juegosDescargando.includes(juegoId)) return "descargando";
    if (progresoDescarga[juegoId] === 100) return "instalado";
    return "pendiente";
  };

  const comprarJuego = async (juegoId) => {
    try {
      const res = await fetch("http://127.0.0.1:8080/api/adquirir", { 
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ juego_id: juegoId }) 
      });
      if (res.ok) { 
        cargarDatos(); 
        iniciarInstalacion(juegoId); 
        cambiarVista("biblioteca"); 
      }
    } catch (e) { 
      console.error("Error compra:", e); 
    }
  };

  const toggleFavorito = (juegoId) => {
    setFavoritosIds(prev => prev.includes(juegoId) ? prev.filter(id => id !== juegoId) : [...prev, juegoId]);
  };

  // Empaquetado de props para las tarjetas
  const propsTarjeta = { 
    obtenerEstadoInst, 
    progresoDescarga, 
    iniciarInstalacion, 
    irADetalle: (j) => cambiarVista("detalle", j) 
  };
  
  // Categorías de la Tienda
  const juegosBanner = juegosLista.slice(0, 8); 
  const masPopulares = juegosLista.filter(j => j.puntuacion >= 4.7);
  const mundoAbierto = juegosLista.filter(j => j.tag === 'Mundo Abierto' || j.tag === 'RPG' || j.tag === 'Supervivencia'); 
  const estrenosRecientes = [...juegosLista].reverse().slice(0, 15);

  let juegosFiltrados = juegosLista;
  if (textoBusqueda) {
    juegosFiltrados = juegosFiltrados.filter(j => 
      j.titulo.toLowerCase().includes(textoBusqueda.toLowerCase()) || 
      j.desarrollador.toLowerCase().includes(textoBusqueda.toLowerCase())
    );
  }
  if (filtroTag !== "Todos") juegosFiltrados = juegosFiltrados.filter(j => j.tag === filtroTag);

  // Categorías y Filtros de la Biblioteca
  let bibliotecaFiltrada = bibliotecaUsuario || [];
  if (pestanaBiblioteca === "favoritos") bibliotecaFiltrada = bibliotecaFiltrada.filter(j => favoritosIds.includes(j.id));
  if (busquedaBiblioteca) bibliotecaFiltrada = bibliotecaFiltrada.filter(j => j.titulo.toLowerCase().includes(busquedaBiblioteca.toLowerCase()));
  if (filtroGeneroBiblio !== "Todos") bibliotecaFiltrada = bibliotecaFiltrada.filter(j => j.tag === filtroGeneroBiblio);
  if (filtroCaracteristica !== "Todas") bibliotecaFiltrada = bibliotecaFiltrada.filter(j => j.caracteristicas.includes(filtroCaracteristica));
  if (filtroPlataforma !== "Todas") bibliotecaFiltrada = bibliotecaFiltrada.filter(j => j.plataformas.includes(filtroPlataforma));

  const contarGen = (tag) => (bibliotecaUsuario || []).filter(j => j.tag === tag).length;
  const contarCar = (carac) => (bibliotecaUsuario || []).filter(j => j.caracteristicas.includes(carac)).length;
  const contarPlat = (plat) => (bibliotecaUsuario || []).filter(j => j.plataformas.includes(plat)).length;

  // ============================================================================
  // RENDERIZADO VISUAL
  // ============================================================================
  return (
    <div className="app-container">
      
      {/* BARRA LATERAL IZQUIERDA */}
      <nav className="sidebar">
        <div className="logo-container" onClick={() => cambiarVista("inicio")}>
          <img src={logoImg} alt="RetroGeek Logo" className="logo-imagen" title="Ir al Inicio" />
        </div>
        <div className="menu-botones">
          <button className={vistaActiva === "inicio" || vistaActiva === "explora" || vistaActiva === "noticias" ? "activo" : ""} onClick={() => cambiarVista("inicio")}>🏪 Tienda</button>
          <button className={vistaActiva === "biblioteca" ? "activo" : ""} onClick={() => cambiarVista("biblioteca")}>📚 Biblioteca</button>
          <button className={vistaActiva === "evaluar" ? "activo" : ""} onClick={() => cambiarVista("evaluar")}>⚙️ Evaluar PC</button>
        </div>
      </nav>

      {/* CONTENIDO CENTRAL */}
      <main className="main-content">
        <header className="top-nav">
          <div className="search-bar">
            🔍 <input type="text" placeholder="Buscar en tienda..." value={textoBusqueda} onChange={(e) => setTextoBusqueda(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && cambiarVista("explora")} />
          </div>
          <div className="nav-links">
            <span className={vistaActiva === "inicio" ? "activo" : ""} onClick={() => cambiarVista("inicio")}>Descubre</span>
            <span className={vistaActiva === "explora" ? "activo" : ""} onClick={() => cambiarVista("explora")}>Explora</span>
            <span className={vistaActiva === "noticias" ? "activo" : ""} onClick={() => cambiarVista("noticias")}>Noticias</span>
          </div>
        </header>

        {cargando && <h2 className="mensaje-carga">Conectando con Servidor Python...</h2>}

        {/* --- VISTA: INICIO --- */}
        {!cargando && vistaActiva === "inicio" && (
          <section className="vista-inicio animate-fade-in">
            {juegosLista.length > 0 && (
              <>
                <div className="hero-container-v2" onClick={() => cambiarVista("detalle", juegosBanner[indiceBanner])}>
                  <img src={juegosBanner[indiceBanner].imagen_url} alt="Banner" className="hero-image animate-fade" />
                  <div className="hero-content animate-fade">
                    <div className="hero-text-area">
                      <h3>DESTACADO DE LA SEMANA</h3>
                      <h1>{juegosBanner[indiceBanner].titulo}</h1>
                      <p className="descripcion-corta">Descubre este título de <strong>{juegosBanner[indiceBanner].tag}</strong> por <strong>{juegosBanner[indiceBanner].desarrollador}</strong>.</p>
                      <button className="btn-hero-profesional">Ver detalles</button>
                    </div>
                  </div>
                  <button className="btn-banner-nav prev" onClick={(e) => { e.stopPropagation(); setIndiceBanner(p => p === 0 ? juegosBanner.length - 1 : p - 1); }}>&#10094;</button>
                  <button className="btn-banner-nav next" onClick={(e) => { e.stopPropagation(); setIndiceBanner(p => (p + 1) % juegosBanner.length); }}>&#10095;</button>
                </div>
                <div className="catalogo-secciones">
                  <FilaJuegos titulo="Lo Más Popular 🔥" juegos={masPopulares} onVerMas={(t, j) => cambiarVista("categoria", {titulo: t, juegos: j})} propsTarjeta={propsTarjeta} />
                  <FilaJuegos titulo="Estrenos Recientes 🚀" juegos={estrenosRecientes} onVerMas={(t, j) => cambiarVista("categoria", {titulo: t, juegos: j})} propsTarjeta={propsTarjeta} />
                  <FilaJuegos titulo="Explora Mundos Abiertos 🌍" juegos={mundoAbierto} onVerMas={(t, j) => cambiarVista("categoria", {titulo: t, juegos: j})} propsTarjeta={propsTarjeta} />
                </div>
              </>
            )}
          </section>
        )}

        {/* --- VISTA: EXPLORA --- */}
        {!cargando && vistaActiva === "explora" && (
          <section className="vista-explora animate-fade-in">
            <h1>Explora el Catálogo</h1>
            <div className="explora-layout">
              <aside className="panel-filtros-tienda">
                <h3>Filtros</h3>
                <div className="grupo-filtro">
                  <label>Género</label>
                  <select value={filtroTag} onChange={(e) => setFiltroTag(e.target.value)}>
                    <option value="Todos">Todos</option>
                    <option value="Shooter">Shooter</option>
                    <option value="RPG">RPG</option>
                    <option value="Mundo Abierto">Mundo Abierto</option>
                    <option value="Indie">Indie</option>
                  </select>
                </div>
              </aside>
              <div className="explora-resultados">
                <div className="grid-juegos-completo">
                  {juegosFiltrados.map((j) => (
                    <TarjetaJuego key={j.id} juego={j} estadoInstalacion={obtenerEstadoInst(j.id)} progreso={progresoDescarga[j.id]} onInstalar={iniciarInstalacion} onClick={(j) => cambiarVista("detalle", j)} />
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* --- VISTA: BIBLIOTECA --- */}
        {!cargando && vistaActiva === "biblioteca" && (
          <section className="vista-biblioteca animate-fade-in">
            <div className="biblioteca-tabs">
              <span className={pestanaBiblioteca === "todos" ? "activo" : ""} onClick={() => setPestanaBiblioteca("todos")}>Todos</span>
              <span className={pestanaBiblioteca === "favoritos" ? "activo" : ""} onClick={() => setPestanaBiblioteca("favoritos")}>Favoritos</span>
            </div>
            
            <div className="biblioteca-layout">
              <div className="biblioteca-contenido-principal">
                <div className="biblioteca-controles">
                  <div className="ordenar-por">Ordenar por: <strong>Recientes ⌄</strong></div>
                  <div className="vistas-toggle">
                    <button className={vistaBiblioteca === "grid" ? "activo" : ""} onClick={() => setVistaBiblioteca("grid")}>⊞</button>
                    <button className={vistaBiblioteca === "lista" ? "activo" : ""} onClick={() => setVistaBiblioteca("lista")}>𝄘</button>
                  </div>
                </div>

                {(juegosDescargando.length > 0 || Object.values(progresoDescarga).some(p => p > 0 && p < 100)) && (
                  <div className="gestor-instalaciones">
                    <h2>Descargas Activas</h2>
                    {(bibliotecaUsuario || []).filter(j => progresoDescarga[j.id] > 0 && progresoDescarga[j.id] < 100).map(j => (
                      <div key={j.id} className="item-descarga">
                        <img src={j.imagen_url} alt="Logo" className="img-descarga" />
                        <div className="info-descarga">
                          <h3>{j.titulo}</h3>
                          <p className="estado-texto">Instalando...</p>
                          <div className="barra-progreso-grande">
                            <div className="progreso-lleno" style={{width: `${progresoDescarga[j.id]}%`}}></div>
                          </div>
                        </div>
                        <span className="porcentaje-grande">{progresoDescarga[j.id]}%</span>
                      </div>
                    ))}
                  </div>
                )}

                <div className={`grid-juegos-completo ${vistaBiblioteca === "lista" ? "modo-lista" : ""}`}>
                  {bibliotecaFiltrada.map((j) => (
                    <TarjetaJuego 
                      key={j.id} 
                      juego={j} 
                      enBiblioteca={true} 
                      vista={vistaBiblioteca} 
                      esFavorito={favoritosIds.includes(j.id)} 
                      onToggleFavorito={toggleFavorito} 
                      estadoInstalacion={obtenerEstadoInst(j.id)} 
                      progreso={progresoDescarga[j.id]} 
                      onInstalar={iniciarInstalacion} 
                      onClick={(j) => cambiarVista("detalle", j)} 
                    />
                  ))}
                </div>
              </div>

              <aside className="biblioteca-sidebar">
                <h3>Filtros</h3>
                <div className="search-bar-local">
                  🔍 <input type="text" placeholder="Buscar..." value={busquedaBiblioteca} onChange={(e) => setBusquedaBiblioteca(e.target.value)} />
                </div>
                
                <details className="filtro-acordeon" open>
                  <summary>Género</summary>
                  <div className="acordeon-contenido">
                    <p onClick={() => setFiltroGeneroBiblio("Todos")}>Todos</p>
                    <p onClick={() => setFiltroGeneroBiblio("Shooter")}>Shooter ({contarGen("Shooter")})</p>
                    <p onClick={() => setFiltroGeneroBiblio("RPG")}>RPG ({contarGen("RPG")})</p>
                    <p onClick={() => setFiltroGeneroBiblio("Mundo Abierto")}>Mundo Abierto ({contarGen("Mundo Abierto")})</p>
                  </div>
                </details>
                
                <details className="filtro-acordeon" open>
                  <summary>Características</summary>
                  <div className="acordeon-contenido">
                    <p onClick={() => setFiltroCaracteristica("Todas")}>Todas</p>
                    <p onClick={() => setFiltroCaracteristica("Logros")}>Logros ({contarCar("Logros")})</p>
                    <p onClick={() => setFiltroCaracteristica("Online Multiplayer")}>Online Multiplayer ({contarCar("Online Multiplayer")})</p>
                  </div>
                </details>
              </aside>
            </div>
          </section>
        )}

        {/* --- VISTA: NOTICIAS --- */}
        {vistaActiva === "noticias" && (
          <section className="vista-noticias animate-fade-in">
            <h1>Noticias Gaming</h1>
            <div className="lista-noticias">
              {NOTICIAS_DB.map((n) => (
                <article key={n.id} className="tarjeta-noticia">
                  <img src={n.img} alt="N" className="noticia-img" />
                  <div className="noticia-contenido">
                    <span className="noticia-fecha">{n.fecha}</span>
                    <h2>{n.titulo}</h2>
                    <p>{n.extracto}</p>
                    <button className="btn-secundario">Leer más</button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* --- VISTA: CATEGORÍA --- */}
        {!cargando && vistaActiva === "categoria" && (
          <section className="vista-categoria animate-fade-in">
            <button className="btn-volver-grande" onClick={() => window.history.back()}>&#8592; Volver</button>
            <h1>{categoriaActual.titulo}</h1>
            <div className="grid-juegos-completo">
              {categoriaActual.juegos.map((j) => (
                <TarjetaJuego key={j.id} juego={j} estadoInstalacion={obtenerEstadoInst(j.id)} progreso={progresoDescarga[j.id]} onInstalar={iniciarInstalacion} onClick={(j) => cambiarVista("detalle", j)} />
              ))}
            </div>
          </section>
        )}

        {/* --- VISTA: DETALLE DE JUEGO (Importando Módulo) --- */}
        {!cargando && vistaActiva === "detalle" && juegoSeleccionado && (
          <section className="vista-detalle animate-fade-in">
            <button className="btn-volver-grande" onClick={() => window.history.back()} style={{ marginBottom: "15px" }}>&#8592; Volver</button>
            
            {/* === INICIO DEL NUEVO COMPONENTE === */}
            <DetalleAvanzado juegoId={juegoSeleccionado.id} />
            {/* === FIN DEL NUEVO COMPONENTE === */}

            {/* SE OCULTA EL CÓDIGO ANTERIOR PARA NO BORRARLO, EXACTAMENTE COMO LO SOLICITASTE */}
            <div style={{ display: "none" }}>
              <div className="detalle-layout">
                
                <div className="columna-principal">
                  <div className="media-placeholder" style={{ backgroundImage: `url('${juegoSeleccionado.imagen_url}')` }}></div>
                  
                  {/* AQUI ESTAMOS LLAMANDO AL ARCHIVO EXTERNO DE TELEMETRÍA */}
                  <PanelHardwareJuego 
                    onAnalisisCompletado={(mensajeIA) => {
                      setMensajeIA(mensajeIA);
                      setChatAbierto(true);
                    }} 
                  />

                </div>

                <div className="columna-lateral">
                  <img src={juegoSeleccionado.imagen_url} alt="Poster" className="poster-detalle" />
                  <h2>{juegoSeleccionado.titulo}</h2>
                  <div className="caja-compra">
                    {juegoSeleccionado.comprado ? (
                      <div className="estado-propiedad">
                        <p className="txt-propiedad">✅ Este juego ya es tuyo</p>
                        <button className="btn-secundario" onClick={() => cambiarVista("biblioteca")}>Ir a Biblioteca</button>
                      </div>
                    ) : (
                      <>
                        <div className="precio-grande">{juegoSeleccionado.precio === 0 ? "Gratis" : `$${juegoSeleccionado.precio}`}</div>
                        <button className="btn-comprar" onClick={() => comprarJuego(juegoSeleccionado.id)}>Obtener ahora</button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* --- VISTA: EVALUAR PC GLOBAL (Importando Módulo) --- */}
        {vistaActiva === "evaluar" && <VistaEvaluarPC />}

      </main>

      {/* CHATBOT */}
      <div className={`chatbot-container ${chatAbierto ? "abierto" : ""}`}>
        {chatAbierto && (
          <div className="chatbot-window">
            <div className="chat-header">Asistente IA</div>
            <div className="chat-mensajes">
              <p className="mensaje-ia"><strong>IA:</strong> {mensajeIA}</p>
            </div>
            <div className="chat-input-area">
              <input type="text" placeholder="Pregunta..." />
              <button>Ir</button>
            </div>
          </div>
        )}
        <button className="btn-chat-toggle" onClick={() => setChatAbierto(!chatAbierto)}>🤖 IA</button>
      </div>
    </div>
  );
}

export default App;