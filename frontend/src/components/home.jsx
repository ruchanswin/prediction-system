import './components.css';
import farePredictionImage from '../../../img/fare_prediction.png';
import delayPredictionImage from '../../../img/delay_prediction.png';

const showcases = [
  {
    title: 'Flight Fare Prediction',
    description:
      'Explore estimated airfare with a prediction experience built around your route, travel dates, and flight preferences.',
    image: farePredictionImage,
    imageAlt: 'FlightForesight fare prediction form and flight results',
    href: '/fare',
    action: 'Explore fare prediction',
    className: 'fare',
  },
  {
    title: 'Flight Delay Prediction',
    description:
      'Review estimated arrival delays and see flight details alongside an interactive route visualization.',
    image: delayPredictionImage,
    imageAlt: 'FlightForesight delay prediction form, route map, and flight results',
    href: '/delay',
    action: 'Explore delay prediction',
    className: 'delay',
  },
];

function Home() {
  return (
    <div className="showcase-page">
      <section className="showcase-hero" aria-labelledby="showcase-title">
        <span className="showcase-eyebrow">Flight planning, made clearer</span>
        <h1 id="showcase-title">Meet FlightForesight</h1>
        <p>
          Explore flight fare and delay predictions in one place. Compare travel
          details, view routes, and make more informed plans before you fly.
        </p>
        <div className="showcase-highlights" aria-label="Project features">
          <span>Fare estimates</span>
          <span>Delay insights</span>
          <span>Route visualization</span>
        </div>
      </section>

      <section className="showcase-section" aria-labelledby="showcase-options-title">
        <div className="showcase-section-heading">
          <span className="showcase-eyebrow">Project highlights</span>
          <h2 id="showcase-options-title">See what you can explore</h2>
          <p>Take a closer look at the tools that bring your journey into focus.</p>
        </div>

        <div className="showcase-grid">
          {showcases.map((item) => (
            <article
              className={`showcase-card showcase-card-${item.className}`}
              key={item.title}
            >
              <img
                className="showcase-card-image"
                src={item.image}
                alt={item.imageAlt}
              />
              <div className="showcase-card-content">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <a className="showcase-card-link" href={item.href}>
                  {item.action}
                  <span aria-hidden="true"> &rarr;</span>
                </a>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Home;
