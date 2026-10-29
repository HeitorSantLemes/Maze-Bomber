
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

const features = [
  {
    icon: '🎮',
    title: 'O Jogo',
    description:
      'Conheça o Maze-Bomber, suas mecânicas, desafios e objetivos.',
    link: '/docs/intro',
    button: 'Conhecer o jogo',
  },
  {
    icon: '💻',
    title: 'Desenvolvimento',
    description:
      'Descubra como o projeto foi desenvolvido utilizando Python e Pygame.',
    link: '/docs/intro',
    button: 'Explorar o código',
  },
  {
    icon: '📚',
    title: 'Documentação',
    description:
      'Encontre tutoriais, explicações e informações técnicas do projeto.',
    link: '/docs/intro',
    button: 'Ler documentação',
  },
];

export default function Home() {
  return (
    <Layout
      title="Maze-Bomber"
      description="Documentação oficial do projeto Maze-Bomber"
    >
      <main className={styles.main}>
        {/* Apresentação principal */}
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <span className={styles.eyebrow}>
              DOCUMENTAÇÃO OFICIAL
            </span>

            <h1 className={styles.heroTitle}>
              Maze-<span>Bomber</span>
            </h1>

            <h2 className={styles.subtitle}>
              Explore. Aprenda. Domine o labirinto.
            </h2>

            <p className={styles.description}>
              Bem-vindo à documentação do Maze-Bomber!
              Aqui você encontra tudo sobre o projeto,
              desde sua instalação até as mecânicas
              e os detalhes do desenvolvimento.
            </p>

            <div className={styles.buttons}>
              <Link
                className={styles.primaryButton}
                to="/docs/intro"
              >
                📖 Começar agora
              </Link>

              <Link
                className={styles.secondaryButton}
                to="https://github.com/HeitorSantLemes/Maze-Bomber"
              >
                Ver no GitHub ↗
              </Link>
            </div>
          </div>

          <div className={styles.heroImageContainer}>
            <img
              src="/img/maze-bomber-banner.png"
              alt="Arte oficial do Maze-Bomber"
              className={styles.heroImage}
            />
          </div>
        </section>

        {/* Apresentação das funcionalidades */}
        <section className={styles.featuresSection}>
          <div className={styles.sectionHeading}>
            <span className={styles.eyebrow}>
              EXPLORE O PROJETO
            </span>

            <h2>Conheça o universo Maze-Bomber</h2>

            <p>
              Tudo o que você precisa para conhecer,
              compreender e explorar o projeto.
            </p>
          </div>

          <div className={styles.features}>
            {features.map((feature) => (
              <article
                className={styles.featureCard}
                key={feature.title}
              >
                <div className={styles.featureIcon}>
                  {feature.icon}
                </div>

                <h3>{feature.title}</h3>

                <p>{feature.description}</p>

                <Link
                  className={styles.featureLink}
                  to={feature.link}
                >
                  {feature.button} →
                </Link>
              </article>
            ))}
          </div>
        </section>

        {/* Seção sobre o projeto */}
        <section className={styles.aboutSection}>
          <div className={styles.aboutContent}>
            <span className={styles.eyebrow}>
              SOBRE O PROJETO
            </span>

            <h2>Mais do que um jogo de labirinto</h2>

            <p>
              O Maze-Bomber é um projeto que combina
              diversão, estratégia e desenvolvimento
              de software. Explore o labirinto, utilize
              bombas para superar obstáculos e conheça
              os detalhes técnicos por meio desta
              documentação.
            </p>

            <Link
              className={styles.primaryButton}
              to="/docs/intro"
            >
              Explorar documentação →
            </Link>
          </div>
        </section>

        {/* Blog */}
        <section className={styles.blogSection}>
          <div>
            <span className={styles.eyebrow}>
              NOVIDADES
            </span>

            <h2>Acompanhe o desenvolvimento</h2>

            <p>
              Confira novidades, atualizações e
              informações sobre o Maze-Bomber.
            </p>
          </div>

          <Link
            className={styles.secondaryButton}
            to="/blog"
          >
            Acessar o blog →
          </Link>
        </section>
      </main>
    </Layout>
  );
}
