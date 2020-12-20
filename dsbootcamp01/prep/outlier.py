def outlier_thresholds(dataframe, variable):

    """

    Calculates thresholds for given variables

    Parameters
    ----------

    dataframe: dataframe
       dataframe that include variables

       col_name: string
          the variable whose threshold is to be calculated
    variable

    Returns
    -------
    float or tuple

    Examples
    -------
     import seaborn as sns
     df=sns.load_dataset("titanic")
     low,up=outlier_thresholds(df,"age")
     print(low,up)
    """

    quartile1 = dataframe[variable].quantile(0.25)
    quartile3 = dataframe[variable].quantile(0.75)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def check_outlier(dataframe,col_name):
    low_limit,up_limit=outlier_thresholds(dataframe,col_name)
    if dataframe[(dataframe[col_name]>up_limit)| (dataframe[col_name]< low_limit)].any(axis=None):
        print(col_name,"yes")
    else:
        print(col_name,"No")


def check_outlier_adv(dataframe,num_columns,plot=False):
    variable_names=[] #aykiri degere sahip degiskenleri tutacak.
    for col in num_columns:
         low_limit,up_limit=outlier_thresholds(dataframe,col)
         if dataframe[(dataframe[col]>up_limit)| (dataframe[col]< low_limit)].any(axis=None):
             number_of_outliers=dataframe[(dataframe[col]> up_limit) |(dataframe[col]<low_limit)].shape[0]
             print(col,":",number_of_outliers)
             variable_names.append(col)
             if plot:
                  sns.boxplot(x=dataframe[col])
                  plt.show()
    return variable_names


def grab_outliers(dataframe,col_name,index=False):
    low,up=outlier_thresholds(dataframe,col_name)
    if dataframe[((dataframe[col_name]<low) | (dataframe[col_name]> up))].shape[0]>10:
        print(dataframe[((dataframe[col_name]<low) | (dataframe[col_name]>up))].head())
    else:
        print(dataframe[((dataframe[col_name]< low) | (dataframe[col_name]>up))])

    if index:
        outlier_index=dataframe[((dataframe[col_name]< low)) | (dataframe[col_name]>up)].index
        return outlier_index

    def remove_outliers(dataframe, variable):
        low_limit, up_limit = outlier_thresholds(dataframe, variable)
        df_without_outliers = dataframe[~((dataframe[variable] < low_limit) | (dataframe[variable] > up_limit))]
        return df_without_outliers

    def replace_with_thresholds(dataframe, variable):
        low_limit, up_limit = outlier_thresholds(dataframe, variable)
        dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
        dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit