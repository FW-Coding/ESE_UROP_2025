import os

import numpy as np

import pybamm

def graphite_diffusivity_Dualfoil1998(sto, T):
    """
    Graphite diffusivity as a function of stoichiometry [1, 2, 3].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Rieger, B., Erhard, S. V., Rumpf, K., & Jossen, A. (2016).
     A new method to model the thickness change of a commercial pouch cell
     during discharge. Journal of The Electrochemical Society, 163(8), A1566-A1575.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry
    T: :class:`pybamm.Symbol`
        Dimensional temperature, [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity [m2.s-1]
    """
    D_ref = 3.9 * 10 ** (-14)
    E_D_s = 5000
    T_ref = 298.15
    arrhenius = np.exp(E_D_s / pybamm.constants.R * (1 / T_ref - 1 / T))
    return D_ref * arrhenius


def graphite_electrolyte_exchange_current_density_Dualfoil1998(
    c_e, c_s_surf, c_s_max, T
):
    """
    Exchange-current density for Butler-Volmer reactions between graphite and LiPF6 in
    EC:DMC.

    References
    ----------
    .. [2] John Newman, Dualfoil

    Parameters
    ----------
    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_s_surf : :class:`pybamm.Symbol`
        Particle concentration [mol.m-3]
    c_s_max : :class:`pybamm.Symbol`
        Maximum particle concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """
    m_ref = (
        1 * 10 ** (-11) * pybamm.constants.F
    )  # (A/m2)(m3/mol)**1.5 - includes ref concentrations
    E_r = 5000  # activation energy for Temperature Dependent Reaction Constant [J/mol]
    arrhenius = np.exp(E_r / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) ** 0.5


def graphite_entropy_Enertech_Ai2020_function(sto):
    """
    Lithium Cobalt Oxide (LiCO2) entropic change in open-circuit potential (OCP) at
    a temperature of 298.15K as a function of the stoichiometry. The fit is taken
    from Ref [1], which is only accurate
    for 0.43 < sto < 0.9936.

    References
    ----------
    .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
    Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
    Lithium-Ion Pouch Cells.
    Journal of The Electrochemical Society, 167(1), 013512. DOI: 10.1149/2.0122001JES

    Parameters
    ----------
    sto: double
       stoichiometry of material (li-fraction)

    Returns
    -------
    :class:`pybamm.Symbol`
        Entropic change [V.K-1]
    """

    du_dT = (
        0.001
        * (
            0.005269056
            + 3.299265709 * sto
            - 91.79325798 * sto**2
            + 1004.911008 * sto**3
            - 5812.278127 * sto**4
            + 19329.7549 * sto**5
            - 37147.8947 * sto**6
            + 38379.18127 * sto**7
            - 16515.05308 * sto**8
        )
        / (
            1
            - 48.09287227 * sto
            + 1017.234804 * sto**2
            - 10481.80419 * sto**3
            + 59431.3 * sto**4
            - 195881.6488 * sto**5
            + 374577.3152 * sto**6
            - 385821.1607 * sto**7
            + 165705.8597 * sto**8
        )
    )

    return du_dT


def graphite_volume_change_Ai2020(sto):
    """
    Graphite particle volume change as a function of stoichiometry [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Rieger, B., Erhard, S. V., Rumpf, K., & Jossen, A. (2016).
     A new method to model the thickness change of a commercial pouch cell
     during discharge. Journal of The Electrochemical Society, 163(8), A1566-A1575.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry, dimensionless
        should be R-averaged particle concentration
    c_s_max : :class:`pybamm.Symbol`
        Maximum particle concentration [mol.m-3]

    Returns
    -------
    t_change:class:`pybamm.Symbol`
        volume change, dimensionless, normalised by particle volume
    """
    p1 = 145.907
    p2 = -681.229
    p3 = 1334.442
    p4 = -1415.710
    p5 = 873.906
    p6 = -312.528
    p7 = 60.641
    p8 = -5.706
    p9 = 0.386
    p10 = -4.966e-05
    t_change = (
        p1 * sto**9
        + p2 * sto**8
        + p3 * sto**7
        + p4 * sto**6
        + p5 * sto**5
        + p6 * sto**4
        + p7 * sto**3
        + p8 * sto**2
        + p9 * sto
        + p10
    )
    return t_change


def graphite_cracking_rate_Ai2020(T_dim):
    """
    graphite particle cracking rate as a function of temperature [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Deshpande, R., Verbrugge, M., Cheng, Y. T., Wang, J., & Liu, P. (2012).
     Battery cycle life prediction with coupled chemical degradation and fatigue
     mechanics. Journal of the Electrochemical Society, 159(10), A1730.

    Parameters
    ----------
    T_dim: :class:`pybamm.Symbol`
        temperature, [K]

    Returns
    -------
    k_cr: :class:`pybamm.Symbol`
        cracking rate, [m/(Pa.m0.5)^m_cr]
        where m_cr is another Paris' law constant
    """
    k_cr = 3.9e-20
    T_ref = 298.15
    Eac_cr = pybamm.Parameter(
        "Negative electrode activation energy for cracking rate [J.mol-1]"
    )
    arrhenius = np.exp(Eac_cr / pybamm.constants.R * (1 / T_dim - 1 / T_ref))
    return k_cr * arrhenius


def lico2_diffusivity_Dualfoil1998(sto, T):
    """
    LiCo2 diffusivity as a function of stoichiometry, in this case the
    diffusivity is taken to be a constant. The value is taken from Dualfoil [1].

    References
    ----------
    .. [1] John Newman, Dualfoil

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry
    T: :class:`pybamm.Symbol`
        Dimensional temperature, [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity [m2.s-1]
    """
    D_ref = 5.387 * 10 ** (-15)
    E_D_s = 5000
    T_ref = 298.15
    arrhenius = np.exp(E_D_s / pybamm.constants.R * (1 / T_ref - 1 / T))
    return D_ref * arrhenius


def lico2_electrolyte_exchange_current_density_Dualfoil1998(c_e, c_s_surf, c_s_max, T):
    """
    Exchange-current density for Butler-Volmer reactions between lico2 and LiPF6 in
    EC:DMC.

    References
    ----------
    .. [2] John Newman, Dualfoil

    Parameters
    ----------
    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_s_surf : :class:`pybamm.Symbol`
        Particle concentration [mol.m-3]
    c_s_max : :class:`pybamm.Symbol`
        Maximum particle concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """
    m_ref = 1 * 10 ** (-11) * pybamm.constants.F  # need to match the unit from m/s
    # (A/m2)(m3/mol)**1.5 - includes ref concentrations
    E_r = 5000
    arrhenius = np.exp(E_r / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) ** 0.5


def lico2_entropic_change_Ai2020_function(sto):
    """
    Lithium Cobalt Oxide (LiCO2) entropic change in open-circuit potential (OCP) at
    a temperature of 298.15K as a function of the stoichiometry. The fit is taken
    from Ref [1], which is only accurate
    for 0.43 < sto < 0.9936.

    References
    ----------
    .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
    Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity
    in Lithium-Ion Pouch Cells. Journal of The Electrochemical Society,
        167(1), 013512. DOI: 10.1149/2.0122001JES

    Parameters
    ----------
    sto: double
       stoichiometry of material (li-fraction)

    Returns
    -------
    :class:`pybamm.Symbol`
        Entropic change [V.K-1]
    """

    # Since the equation for LiCo2 from this ref. has the stretch factor,
    # should this too? If not, the "bumps" in the OCV don't line up.
    p1 = -3.20392657
    p2 = 14.5719049
    p3 = -27.9047599
    p4 = 29.1744564
    p5 = -17.992018
    p6 = 6.54799331
    p7 = -1.30382445
    p8 = 0.109667298

    du_dT = (
        p1 * sto**7
        + p2 * sto**6
        + p3 * sto**5
        + p4 * sto**4
        + p5 * sto**3
        + p6 * sto**2
        + p7 * sto
        + p8
    )

    return du_dT


def lico2_volume_change_Ai2020(sto):
    """
    lico2 particle volume change as a function of stoichiometry [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Rieger, B., Erhard, S. V., Rumpf, K., & Jossen, A. (2016).
     A new method to model the thickness change of a commercial pouch cell
     during discharge. Journal of The Electrochemical Society, 163(8), A1566-A1575.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry, dimensionless
        should be R-averaged particle concentration

    Returns
    -------
    t_change:class:`pybamm.Symbol`
        volume change, dimensionless, normalised by particle volume
    """
    omega = pybamm.Parameter("Positive electrode partial molar volume [m3.mol-1]")
    c_s_max = pybamm.Parameter("Maximum concentration in positive electrode [mol.m-3]")
    t_change = omega * c_s_max * sto
    return t_change


def lico2_cracking_rate_Ai2020(T_dim):
    """
    lico2 particle cracking rate as a function of temperature [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Deshpande, R., Verbrugge, M., Cheng, Y. T., Wang, J., & Liu, P. (2012).
     Battery cycle life prediction with coupled chemical degradation and fatigue
     mechanics. Journal of the Electrochemical Society, 159(10), A1730.

    Parameters
    ----------
    T: :class:`pybamm.Symbol`
        temperature, [K]

    Returns
    -------
    k_cr: :class:`pybamm.Symbol`
        cracking rate, [m/(Pa.m0.5)^m_cr]
        where m_cr is another Paris' law constant
    """
    k_cr = 3.9e-20
    T_ref = 298.15
    Eac_cr = pybamm.Parameter(
        "Positive electrode activation energy for cracking rate [J.mol-1]"
    )
    arrhenius = np.exp(Eac_cr / pybamm.constants.R * (1 / T_dim - 1 / T_ref))
    return k_cr * arrhenius


def dlnf_dlnc_Ai2020(c_e, T, T_ref=298.3, t_plus=0.38):
    """
    Activity dependence of LiPF6 in EC:DMC as a function of ion concentration.

    References
    ----------
    .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
    Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity
    in Lithium-Ion Pouch Cells. Journal of The Electrochemical Society,
    167(1), 013512. DOI: 10.1149/2.0122001JES.

    Parameters
    ----------
    c_e: :class:`pybamm.Symbol`
        Dimensional electrolyte concentration, mol/m^3
    T: :class:`pybamm.Symbol`
        Dimensional temperature, K

    Returns
    -------
    :class:`pybamm.Symbol`
        Thermodynamic factor
    """
    T_ref = 298.15
    t_plus = pybamm.Parameter("Cation transference number")
    dlnf_dlnc = (
        0.601
        - 0.24 * (c_e / 1000) ** 0.5
        + 0.982 * (1 - 0.0052 * (T - T_ref)) * (c_e / 1000) ** 1.5
    ) / (1 - t_plus)
    return dlnf_dlnc


def electrolyte_diffusivity_Ai2020(c_e, T):
    """
    Diffusivity of LiPF6 in EC:DMC as a function of ion concentration.

    References
    ----------
    .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
    Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity
    in Lithium-Ion Pouch Cells. Journal of The Electrochemical Society,
    167(1), 013512. DOI: 10.1149/2.0122001JES.

    Parameters
    ----------
    c_e: :class:`pybamm.Symbol`
        Dimensional electrolyte concentration, mol/m^3
    T: :class:`pybamm.Symbol`
        Dimensional temperature, K


    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity
    """

    D_c_e = 10 ** (-4.43 - 54 / (T - 229 - 5e-3 * c_e) - 0.22e-3 * c_e)

    return D_c_e


def electrolyte_conductivity_Ai2020(c_e, T):
    """
    Conductivity of LiPF6 in EC:DMC as a function of ion concentration.
    Concentration should be in dm3 in the function.

    References
    ----------
    .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
    Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity
    in Lithium-Ion Pouch Cells. Journal of The Electrochemical Society,
    167(1), 013512. DOI: 10.1149/2.0122001JES.
    .. [2] Torchio, Marcello, et al. "Lionsimba: a matlab framework based
    on a finite volume model suitable for li-ion battery design, simulation,
    and control." Journal of The Electrochemical Society 163.7 (2016): A1192.

    Parameters
    ----------
    c_e: :class:`pybamm.Symbol`
        Dimensional electrolyte concentration
    T: :class:`pybamm.Symbol`
        Dimensional temperature

    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity
    """

    sigma_e = (
        1e-4
        * c_e
        * (
            (-10.5 + 0.668 * 1e-3 * c_e + 0.494 * 1e-6 * c_e**2)
            + (0.074 - 1.78 * 1e-5 * c_e - 8.86 * 1e-10 * c_e**2) * T
            + (-6.96 * 1e-5 + 2.8 * 1e-8 * c_e) * T**2
        )
        ** 2
    )

    return sigma_e


# Load data in the appropriate format
path, _ = os.path.split(os.path.abspath(__file__))
graphite_ocp_Enertech_Ai2020_data = pybamm.parameters.process_1D_data(
    "graphite_ocp_Enertech_Ai2020.csv", path=path
)
lico2_ocp_Ai2020_data = pybamm.parameters.process_1D_data(
    "lico2_ocp_Ai2020.csv", path=path
)


def graphite_ocp_Enertech_Ai2020(sto):
    name, (x, y) = graphite_ocp_Enertech_Ai2020_data
    return pybamm.Interpolant(x, y, sto, name=name, interpolator="cubic")


def lico2_ocp_Ai2020(sto):
    name, (x, y) = lico2_ocp_Ai2020_data
    return pybamm.Interpolant(x, y, sto, name=name, interpolator="cubic")


def plating_exchange_current_density_OKane2020(c_e, c_Li, T):
    """
    Exchange-current density for Li plating reaction [A.m-2].
    References
    ----------
    .. [1] O’Kane, Simon EJ, Ian D. Campbell, Mohamed WJ Marzook, Gregory J. Offer, and
    Monica Marinescu. "Physical origin of the differential voltage minimum associated
    with lithium plating in Li-ion batteries." Journal of The Electrochemical Society
    167, no. 9 (2020): 090540.
    Parameters
    ----------
    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_Li : :class:`pybamm.Symbol`
        Plated lithium concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]
    Returns
    -------
    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """

    k_plating = pybamm.Parameter("Lithium plating kinetic rate constant [m.s-1]")

    return pybamm.constants.F * k_plating * c_e


def stripping_exchange_current_density_OKane2020(c_e, c_Li, T):
    """
    Exchange-current density for Li stripping reaction [A.m-2].

    References
    ----------

    .. [1] O’Kane, Simon EJ, Ian D. Campbell, Mohamed WJ Marzook, Gregory J. Offer, and
    Monica Marinescu. "Physical origin of the differential voltage minimum associated
    with lithium plating in Li-ion batteries." Journal of The Electrochemical Society
    167, no. 9 (2020): 090540.

    Parameters
    ----------

    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_Li : :class:`pybamm.Symbol`
        Plated lithium concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]

    Returns
    -------

    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """

    k_plating = pybamm.Parameter("Lithium plating kinetic rate constant [m.s-1]")

    return pybamm.constants.F * k_plating * c_Li


def SEI_limited_dead_lithium_OKane2022(L_sei):
    """
    Decay rate for dead lithium formation [s-1].
    References
    ----------
    .. [1] Simon E. J. O'Kane, Weilong Ai, Ganesh Madabattula, Diega Alonso-Alvarez,
    Robert Timms, Valentin Sulzer, Jaqueline Sophie Edge, Billy Wu, Gregory J. Offer
    and Monica Marinescu. "Lithium-ion battery degradation: how to model it."
    Physical Chemistry: Chemical Physics 24, no. 13 (2022): 7909-7922.
    Parameters
    ----------
    L_sei : :class:`pybamm.Symbol`
        Total SEI thickness [m]
    Returns
    -------
    :class:`pybamm.Symbol`
        Dead lithium decay rate [s-1]
    """

    gamma_0 = pybamm.Parameter("Dead lithium decay constant [s-1]")
    L_sei_0 = pybamm.Parameter("Initial SEI thickness [m]")

    gamma = gamma_0 * L_sei_0 / L_sei

    return gamma


def graphite_LGM50_diffusivity_Chen2020(sto, T):
    """
    LG M50 Graphite diffusivity as a function of stoichiometry, in this case the
    diffusivity is taken to be a constant. The value is taken from [1].

    References
    ----------
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the
    Electrochemical Society 167 (2020): 080534.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
       Electrode stoichiometry
    T: :class:`pybamm.Symbol`
       Dimensional temperature

    Returns
    -------
    :class:`pybamm.Symbol`
       Solid diffusivity
    """

    D_ref = 3.3e-14
    E_D_s = 3.03e4
    # E_D_s not given by Chen et al (2020), so taken from Ecker et al. (2015) instead
    arrhenius = np.exp(E_D_s / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return D_ref * arrhenius


def graphite_LGM50_electrolyte_exchange_current_density_Chen2020(
    c_e, c_s_surf, c_s_max, T
):
    """
    Exchange-current density for Butler-Volmer reactions between graphite and LiPF6 in
    EC:DMC.

    References
    ----------
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the
    Electrochemical Society 167 (2020): 080534.

    Parameters
    ----------
    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_s_surf : :class:`pybamm.Symbol`
        Particle concentration [mol.m-3]
    c_s_max : :class:`pybamm.Symbol`
        Maximum particle concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """

    m_ref = 6.48e-7  # (A/m2)(m3/mol)**1.5 - includes ref concentrations
    E_r = 35000
    arrhenius = np.exp(E_r / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) ** 0.5


def graphite_volume_change_Ai2020(sto):
    """
    Graphite particle volume change as a function of stoichiometry [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Rieger, B., Erhard, S. V., Rumpf, K., & Jossen, A. (2016).
     A new method to model the thickness change of a commercial pouch cell
     during discharge. Journal of The Electrochemical Society, 163(8), A1566-A1575.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry, dimensionless
        should be R-averaged particle concentration
    Returns
    -------
    t_change:class:`pybamm.Symbol`
        volume change, dimensionless, normalised by particle volume
    """
    p1 = 145.907
    p2 = -681.229
    p3 = 1334.442
    p4 = -1415.710
    p5 = 873.906
    p6 = -312.528
    p7 = 60.641
    p8 = -5.706
    p9 = 0.386
    p10 = -4.966e-05
    t_change = (
        p1 * sto**9
        + p2 * sto**8
        + p3 * sto**7
        + p4 * sto**6
        + p5 * sto**5
        + p6 * sto**4
        + p7 * sto**3
        + p8 * sto**2
        + p9 * sto
        + p10
    )
    return t_change


def graphite_cracking_rate_Ai2020(T_dim):
    """
    Graphite particle cracking rate as a function of temperature [1, 2].

    References
    ----------
     .. [1] Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] Deshpande, R., Verbrugge, M., Cheng, Y. T., Wang, J., & Liu, P. (2012).
     Battery cycle life prediction with coupled chemical degradation and fatigue
     mechanics. Journal of the Electrochemical Society, 159(10), A1730.

    Parameters
    ----------
    T_dim: :class:`pybamm.Symbol`
        temperature, [K]

    Returns
    -------
    k_cr: :class:`pybamm.Symbol`
        cracking rate, [m/(Pa.m0.5)^m_cr]
        where m_cr is another Paris' law constant
    """
    k_cr = 3.9e-20
    Eac_cr = 0  # to be implemented
    arrhenius = np.exp(Eac_cr / pybamm.constants.R * (1 / T_dim - 1 / 298.15))
    return k_cr * arrhenius


def nmc_LGM50_diffusivity_Chen2020(sto, T):
    """
     NMC diffusivity as a function of stoichiometry, in this case the
     diffusivity is taken to be a constant. The value is taken from [1].

     References
     ----------
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the
    Electrochemical Society 167 (2020): 080534.

     Parameters
     ----------
     sto: :class:`pybamm.Symbol`
       Electrode stoichiometry
     T: :class:`pybamm.Symbol`
        Dimensional temperature

     Returns
     -------
     :class:`pybamm.Symbol`
        Solid diffusivity
    """

    D_ref = 4e-15
    E_D_s = 25000  # O'Kane et al. (2022), after Cabanero et al. (2018)
    arrhenius = np.exp(E_D_s / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return D_ref * arrhenius


def nmc_LGM50_ocp_Chen2020(sto):
    """
    LG M50 NMC open-circuit potential as a function of stoichiometry, fit taken
    from [1].

    References
    ----------
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the
    Electrochemical Society 167 (2020): 080534.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry

    Returns
    -------
    :class:`pybamm.Symbol`
        Open-circuit potential
    """

    u_eq = (
        -0.8090 * sto
        + 4.4875
        - 0.0428 * np.tanh(18.5138 * (sto - 0.5542))
        - 17.7326 * np.tanh(15.7890 * (sto - 0.3117))
        + 17.5842 * np.tanh(15.9308 * (sto - 0.3120))
    )

    return u_eq


def nmc_LGM50_electrolyte_exchange_current_density_Chen2020(c_e, c_s_surf, c_s_max, T):
    """
    Exchange-current density for Butler-Volmer reactions between NMC and LiPF6 in
    EC:DMC.

    References
    ----------
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the
    Electrochemical Society 167 (2020): 080534.

    Parameters
    ----------
    c_e : :class:`pybamm.Symbol`
        Electrolyte concentration [mol.m-3]
    c_s_surf : :class:`pybamm.Symbol`
        Particle concentration [mol.m-3]
    T : :class:`pybamm.Symbol`
        Temperature [K]

    Returns
    -------
    :class:`pybamm.Symbol`
        Exchange-current density [A.m-2]
    """
    m_ref = 3.42e-6  # (A/m2)(m3/mol)**1.5 - includes ref concentrations
    E_r = 17800
    arrhenius = np.exp(E_r / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) ** 0.5


def volume_change_Ai2020(sto):
    """
    Particle volume change as a function of stoichiometry [1, 2].

    References
    ----------
     .. [1] > Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] > Rieger, B., Erhard, S. V., Rumpf, K., & Jossen, A. (2016).
     A new method to model the thickness change of a commercial pouch cell
     during discharge. Journal of The Electrochemical Society, 163(8), A1566-A1575.

    Parameters
    ----------
    sto: :class:`pybamm.Symbol`
        Electrode stoichiometry, dimensionless
        should be R-averaged particle concentration
    Returns
    -------
    t_change:class:`pybamm.Symbol`
        volume change, dimensionless, normalised by particle volume
    """
    omega = pybamm.Parameter("Positive electrode partial molar volume [m3.mol-1]")
    c_s_max = pybamm.Parameter("Maximum concentration in positive electrode [mol.m-3]")
    t_change = omega * c_s_max * sto
    return t_change


def cracking_rate_Ai2020(T_dim):
    """
    Particle cracking rate as a function of temperature [1, 2].

    References
    ----------
     .. [1] > Ai, W., Kraft, L., Sturm, J., Jossen, A., & Wu, B. (2020).
     Electrochemical Thermal-Mechanical Modelling of Stress Inhomogeneity in
     Lithium-Ion Pouch Cells. Journal of The Electrochemical Society, 167(1), 013512
      DOI: 10.1149/2.0122001JES.
     .. [2] > Deshpande, R., Verbrugge, M., Cheng, Y. T., Wang, J., & Liu, P. (2012).
     Battery cycle life prediction with coupled chemical degradation and fatigue
     mechanics. Journal of the Electrochemical Society, 159(10), A1730.

    Parameters
    ----------
    T: :class:`pybamm.Symbol`
        temperature, [K]

    Returns
    -------
    k_cr: :class:`pybamm.Symbol`
        cracking rate, [m/(Pa.m0.5)^m_cr]
        where m_cr is another Paris' law constant
    """
    k_cr = 3.9e-20
    Eac_cr = 0  # to be implemented
    arrhenius = np.exp(Eac_cr / pybamm.constants.R * (1 / T_dim - 1 / 298.15))
    return k_cr * arrhenius


def electrolyte_diffusivity_Nyman2008_arrhenius(c_e, T):
    """
    Diffusivity of LiPF6 in EC:EMC (3:7) as a function of ion concentration. The data
    comes from [1], with Arrhenius temperature dependence added from [2].

    References
    ----------
    .. [1] A. Nyman, M. Behm, and G. Lindbergh, "Electrochemical characterisation and
    modelling of the mass transport phenomena in LiPF6-EC-EMC electrolyte,"
    Electrochim. Acta, vol. 53, no. 22, pp. 6356–6365, 2008.
    .. [2] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery i. determination of parameters." Journal of the
    Electrochemical Society 162.9 (2015): A1836-A1848.

    Parameters
    ----------
    c_e: :class:`pybamm.Symbol`
        Dimensional electrolyte concentration
    T: :class:`pybamm.Symbol`
        Dimensional temperature

    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity
    """

    D_c_e = 8.794e-11 * (c_e / 1000) ** 2 - 3.972e-10 * (c_e / 1000) + 4.862e-10

    # Nyman et al. (2008) does not provide temperature dependence
    # So use temperature dependence from Ecker et al. (2015) instead

    E_D_c_e = 17000
    arrhenius = np.exp(E_D_c_e / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return D_c_e * arrhenius


def electrolyte_conductivity_Nyman2008_arrhenius(c_e, T):
    """
    Conductivity of LiPF6 in EC:EMC (3:7) as a function of ion concentration. The data
    comes from [1], with Arrhenius temperature dependence added from [2].

    References
    ----------
    .. [1] A. Nyman, M. Behm, and G. Lindbergh, "Electrochemical characterisation and
    modelling of the mass transport phenomena in LiPF6-EC-EMC electrolyte,"
    Electrochim. Acta, vol. 53, no. 22, pp. 6356–6365, 2008.
    .. [2] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery i. determination of parameters." Journal of the
    Electrochemical Society 162.9 (2015): A1836-A1848.

    Parameters
    ----------
    c_e: :class:`pybamm.Symbol`
        Dimensional electrolyte concentration
    T: :class:`pybamm.Symbol`
        Dimensional temperature

    Returns
    -------
    :class:`pybamm.Symbol`
        Solid diffusivity
    """

    sigma_e = (
        0.1297 * (c_e / 1000) ** 3 - 2.51 * (c_e / 1000) ** 1.5 + 3.329 * (c_e / 1000)
    )

    # Nyman et al. (2008) does not provide temperature dependence
    # So use temperature dependence from Ecker et al. (2015) instead

    E_sigma_e = 17000
    arrhenius = np.exp(E_sigma_e / pybamm.constants.R * (1 / 298.15 - 1 / T))

    return sigma_e * arrhenius


# Load data in the appropriate format
path, _ = os.path.split(os.path.abspath(__file__))
graphite_LGM50_ocp_Chen2020_data = pybamm.parameters.process_1D_data(
    "graphite_LGM50_ocp_Chen2020.csv", path=path
)


def graphite_LGM50_ocp_Chen2020(sto):
    name, (x, y) = graphite_LGM50_ocp_Chen2020_data
    return pybamm.Interpolant(x, y, sto, name=name, interpolator="cubic")


# Call dict via a function to avoid errors when editing in place
def get_parameter_values():
    """
    Parameters for an LG M50 cell, from the paper :footcite:t:`OKane2022`, based on the
    paper :footcite:t:`Chen2020` and references therein.

    .. note::
        This parameter set does not claim to be representative of the true parameter
        values. Instead these are parameter values that were used to fit SEI models to
        observed experimental data in the referenced papers.
    """

    return {
        "chemistry": "lithium_ion",
        # lithium plating
        "Lithium metal partial molar volume [m3.mol-1]": 1.3e-05,
        "Lithium plating kinetic rate constant [m.s-1]": 1e-09,
        "Exchange-current density for plating [A.m-2]"
        "": plating_exchange_current_density_OKane2020,
        "Exchange-current density for stripping [A.m-2]"
        "": stripping_exchange_current_density_OKane2020,
        "Initial plated lithium concentration [mol.m-3]": 0.0,
        "Typical plated lithium concentration [mol.m-3]": 1000.0,
        "Lithium plating transfer coefficient": 0.65,
        "Dead lithium decay constant [s-1]": 1e-06,
        "Dead lithium decay rate [s-1]": SEI_limited_dead_lithium_OKane2022,
        # sei
        "Ratio of lithium moles to SEI moles": 1.0,
        "SEI partial molar volume [m3.mol-1]": 9.585e-05,
        "SEI reaction exchange current density [A.m-2]": 1.5e-07,
        "SEI resistivity [Ohm.m]": 200000.0,
        "SEI solvent diffusivity [m2.s-1]": 2.5e-22,
        "Bulk solvent concentration [mol.m-3]": 2636.0,
        "SEI open-circuit potential [V]": 0.4,
        "SEI electron conductivity [S.m-1]": 8.95e-14,
        "SEI lithium interstitial diffusivity [m2.s-1]": 1e-20,
        "Lithium interstitial reference concentration [mol.m-3]": 15.0,
        "Initial SEI thickness [m]": 5e-09,
        "Initial SEI on cracks thickness [m]": 5e-13,  # avoid division by zero
        "EC initial concentration in electrolyte [mol.m-3]": 4541.0,
        "EC diffusivity [m2.s-1]": 2e-18,
        "SEI kinetic rate constant [m.s-1]": 1e-12,
        "SEI growth activation energy [J.mol-1]": 38000.0,
        "Negative electrode reaction-driven LAM factor [m3.mol-1]": 0.0,
        "Positive electrode reaction-driven LAM factor [m3.mol-1]": 0.0,
        # cell
        "Negative current collector thickness [m]": 1.2e-05,
        "Negative electrode thickness [m]": 8.52e-05,
        "Separator thickness [m]": 1.2e-05,
        "Positive electrode thickness [m]": 7.56e-05,
        "Positive current collector thickness [m]": 1.6e-05,
        "Electrode height [m]": 0.065,
        "Electrode width [m]": 1.58,
        "Cell cooling surface area [m2]": 0.00531,
        "Cell volume [m3]": 2.42e-05,
        "Cell thermal expansion coefficient [m.K-1]": 1.1e-06,
        "Negative current collector conductivity [S.m-1]": 58411000.0,
        "Positive current collector conductivity [S.m-1]": 36914000.0,
        "Negative current collector density [kg.m-3]": 8960.0,
        "Positive current collector density [kg.m-3]": 2700.0,
        "Negative current collector specific heat capacity [J.kg-1.K-1]": 385.0,
        "Positive current collector specific heat capacity [J.kg-1.K-1]": 897.0,
        "Negative current collector thermal conductivity [W.m-1.K-1]": 401.0,
        "Positive current collector thermal conductivity [W.m-1.K-1]": 237.0,
        "Nominal cell capacity [A.h]": 5.0,
        "Current function [A]": 5.0,
        "Contact resistance [Ohm]": 0,
        # negative electrode
        "Negative electrode conductivity [S.m-1]": 100.0,
        "Maximum concentration in negative electrode [mol.m-3]": 28700.0,
        "Negative particle diffusivity [m2.s-1]": graphite_diffusivity_Dualfoil1998,
        "Negative electrode OCP [V]": graphite_ocp_Enertech_Ai2020,
        "Negative electrode porosity": 0.33,
        "Negative electrode active material volume fraction": 0.61,
        "Negative particle radius [m]": 5e-06,
        "Negative electrode Bruggeman coefficient (electrolyte)": 2.914,
        "Negative electrode Bruggeman coefficient (electrode)": 0.0,
        "Negative electrode charge transfer coefficient": 0.5,
        "Negative electrode double-layer capacity [F.m-2]": 0.2,
        "Negative electrode exchange-current density [A.m-2]"
        "": graphite_electrolyte_exchange_current_density_Dualfoil1998,
        "Negative electrode density [kg.m-3]": 2470.0,
        "Negative electrode specific heat capacity [J.kg-1.K-1]": 1080.2,
        "Negative electrode thermal conductivity [W.m-1.K-1]": 1.04,
        "Negative electrode OCP entropic change [V.K-1]"
        "": graphite_entropy_Enertech_Ai2020_function,
        "Negative electrode Poisson's ratio": 0.3,
        "Negative electrode Young's modulus [Pa]": 15000000000.0,
        "Negative electrode reference concentration for free of deformation [mol.m-3]"
        "": 0.0,
        "Negative electrode partial molar volume [m3.mol-1]": 3.1e-06,
        "Negative electrode volume change": graphite_volume_change_Ai2020,
        "Negative electrode initial crack length [m]": 2e-08,
        "Negative electrode initial crack width [m]": 1.5e-08,
        "Negative electrode number of cracks per unit area [m-2]": 3180000000000000.0,
        "Negative electrode Paris' law constant b": 1.12,
        "Negative electrode Paris' law constant m": 2.2,
        "Negative electrode cracking rate": graphite_cracking_rate_Ai2020,
        "Negative electrode activation energy for cracking rate [J.mol-1]": 0.0,
        "Negative electrode LAM constant proportional term [s-1]": 0.0,
        "Negative electrode LAM constant exponential term": 2.0,
        "Negative electrode critical stress [Pa]": 60000000.0,
        # positive electrode
        "Positive electrode conductivity [S.m-1]": 0.18,
        "Maximum concentration in positive electrode [mol.m-3]": 63104.0,
        "Positive particle diffusivity [m2.s-1]": nmc_LGM50_diffusivity_Chen2020,
        "Positive electrode OCP [V]": nmc_LGM50_ocp_Chen2020,
        "Positive electrode porosity": 0.335,
        "Positive electrode active material volume fraction": 0.665,
        "Positive particle radius [m]": 5.22e-06,
        "Positive electrode Bruggeman coefficient (electrolyte)": 1.5,
        "Positive electrode Bruggeman coefficient (electrode)": 1.5,
        "Positive electrode charge transfer coefficient": 0.5,
        "Positive electrode double-layer capacity [F.m-2]": 0.2,
        "Positive electrode exchange-current density [A.m-2]"
        "": nmc_LGM50_electrolyte_exchange_current_density_Chen2020,
        "Positive electrode density [kg.m-3]": 3262.0,
        "Positive electrode specific heat capacity [J.kg-1.K-1]": 700.0,
        "Positive electrode thermal conductivity [W.m-1.K-1]": 2.1,
        "Positive electrode OCP entropic change [V.K-1]": 0.0,
        "Positive electrode Poisson's ratio": 0.2,
        "Positive electrode Young's modulus [Pa]": 375000000000.0,
        "Positive electrode reference concentration for free of deformation [mol.m-3]"
        "": 0.0,
        "Positive electrode partial molar volume [m3.mol-1]": 1.25e-05,
        "Positive electrode volume change": volume_change_Ai2020,
        "Positive electrode initial crack length [m]": 2e-08,
        "Positive electrode initial crack width [m]": 1.5e-08,
        "Positive electrode number of cracks per unit area [m-2]": 3180000000000000.0,
        "Positive electrode Paris' law constant b": 1.12,
        "Positive electrode Paris' law constant m": 2.2,
        "Positive electrode cracking rate": cracking_rate_Ai2020,
        "Positive electrode LAM constant proportional term [s-1]": 2.7778e-07,
        "Positive electrode LAM constant exponential term": 2.0,
        "Positive electrode critical stress [Pa]": 375000000.0,
        # separator
        "Separator porosity": 0.47,
        "Separator Bruggeman coefficient (electrolyte)": 1.5,
        "Separator density [kg.m-3]": 397.0,
        "Separator specific heat capacity [J.kg-1.K-1]": 700.0,
        "Separator thermal conductivity [W.m-1.K-1]": 0.16,
        # electrolyte
        "Initial concentration in electrolyte [mol.m-3]": 1000.0,
        "Cation transference number": 0.2594,
        "Thermodynamic factor": 1.0,
        "Electrolyte diffusivity [m2.s-1]": electrolyte_diffusivity_Nyman2008_arrhenius,
        "Electrolyte conductivity [S.m-1]"
        "": electrolyte_conductivity_Nyman2008_arrhenius,
        # experiment
        "Reference temperature [K]": 298.15,
        "Total heat transfer coefficient [W.m-2.K-1]": 10.0,
        "Ambient temperature [K]": 298.15,
        "Number of electrodes connected in parallel to make a cell": 1.0,
        "Number of cells connected in series to make a battery": 1.0,
        "Lower voltage cut-off [V]": 2.5,
        "Upper voltage cut-off [V]": 4.2,
        "Open-circuit voltage at 0% SOC [V]": 2.5,
        "Open-circuit voltage at 100% SOC [V]": 4.2,
        "Initial concentration in negative electrode [mol.m-3]": 29866.0,
        "Initial concentration in positive electrode [mol.m-3]": 17038.0,
        "Initial temperature [K]": 298.15,
        # citations
        "citations": ["OKane2022", "OKane2020", "Chen2020", "Ai2020"],
    }