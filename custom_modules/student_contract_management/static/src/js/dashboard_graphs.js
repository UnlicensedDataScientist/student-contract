odoo.define("student_contract_management.dashboard_graphs", function (require) {
  "use strict";

  // Colores unificados para todos los gráficos
  const unifiedColors = [
    "#FF6384",
    "#36A2EB",
    "#FFCE56",
    "#4BC0C0",
    "#9966FF",
    "#FF9F40",
  ];

  // Función para inicializar y renderizar los gráficos
  function renderCharts() {
    fetch("/dashboard/data")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error al obtener los datos");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Datos recibidos:", data);

        renderChart("genderChart", data.gender_distribution, "pie");
        renderChart("paymentStatusChart", data.payment_status, "bar");
        renderChart("departmentsChart", data.departments, "doughnut");
        renderBarChartWithGradient(
          "subjectsByStudentChart",
          data.subjects_by_student,
          "bar"
        );
        renderBarChartWithGradient(
          "distributionContractsByDepartmentsChart",
          data.contract_by_department,
          "pie"
        );
        renderBarChartWithGradient(
          "distributionContractsByCareerChart",
          data.contract_by_career,
          "pie"
        );
        renderStackedBarChart(
          "subjectsByProfessorChart",
          data.subjects_by_professor
        );
      })
      .catch((error) => {
        console.error("Error al obtener los datos:", error);
        alert(
          "Hubo un problema al cargar los gráficos. Por favor, intente más tarde."
        );
      });
  }

  // Función genérica para renderizar gráficos
  function renderChart(chartId, data, chartType) {
    const chartElement = document.getElementById(chartId);
    if (chartElement) {
      new Chart(chartElement, {
        type: chartType,
        data: {
          labels: data.map((d) => d.label),
          datasets: [
            {
              data: data.map((d) => d.value),
              backgroundColor: unifiedColors.slice(0, data.length), // Usar colores unificados
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return context.raw + " items";
                },
              },
            },
          },
        },
      });
    }
  }

  // Función para renderizar un gráfico de barras con degradado
  function renderBarChartWithGradient(chartId, data, chartType) {
    const chartElement = document.getElementById(chartId);
    if (chartElement) {
      const ctx = chartElement.getContext("2d");

      // Para un gráfico Pie, generar colores únicos para cada segmento
      const colors = data.map(() => getRandomVibrantColor());

      new Chart(chartElement, {
        type: chartType,
        data: {
          labels: data.map((d) => d.label),
          datasets: [
            {
              data: data.map((d) => d.value),
              backgroundColor: colors, // Colores únicos por segmento
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return context.raw + " subjects";
                },
              },
            },
          },
        },
      });
    }
  }

  function getRandomVibrantColor() {
    const randomColor = (min = 50, max = 255) =>
      Math.floor(Math.random() * (max - min + 1) + min)
        .toString(16)
        .padStart(2, "0");

    // Generamos un color más saturado y llamativo
    return `#${randomColor(
      100,
      255
    )}${randomColor(100, 255)}${randomColor(100, 255)}`;
  }

  function renderStackedBarChart(chartId, data) {
    const chartElement = document.getElementById(chartId);
    if (chartElement) {
      const labels = data.map((d) => d.Professor);
      const subjects = Object.keys(data[0]).filter(
        (key) => key !== "Professor"
      );

      const datasets = subjects.map((subject, index) => ({
        label: subject,
        data: data.map((prof) => prof[subject] || 0),
        backgroundColor: unifiedColors[index % unifiedColors.length],
      }));

      new Chart(chartElement, {
        type: "bar",
        data: {
          labels: labels,
          datasets: datasets,
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Subjects Taught by Professors",
            },
          },
          scales: {
            x: { stacked: true },
            y: { stacked: true },
          },
        },
      });
    }
  }

  $(document).ready(function () {
    setTimeout(renderCharts, 500);
    $(document).on("view_change", function () {
      setTimeout(renderCharts, 500);
    });
    setTimeout(function () {
      if (document.activeElement) {
        document.activeElement.blur();
      }
    }, 1000);
  });
});
