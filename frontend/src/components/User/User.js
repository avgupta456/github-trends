import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { getUserData } from '../../api';
import { setUserId, setUserData } from '../../redux/actions/userActions';

class User extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      contribTimeline: [],
    };
  }

  componentDidMount() {
    // TODO: Get GitHub Username
    this.props.setUserId('avgupta456');
  }

  // eslint-disable-next-line no-unused-vars
  componentDidUpdate(prevProps, prevState) {
    if (this.props.userId !== prevProps.userId) {
      (async () => {
        this.setState({ loading: true });
        const userContribs = await getUserData(this.props.userId);
        this.props.setUserData(userContribs);
        this.setState({ loading: false });
      })();
    }

    if (this.props.userData !== prevProps.userData) {
      const contribTimeline = Object.entries(
        this.props.userData.contribs_per_day,
      ).map((x) => {
        console.log(x);
        return { day: x[0], value: x[1] };
      });

      this.setState({ contribTimeline });
    }
  }

  render() {
    const timeline = this.state.contribTimeline;

    return (
      <div style={{ padding: 50 }}>
        <h2>Contribution Timeline</h2>
        <div style={{ height: 400 }}>
          {!this.state.loading && (
            <ResponsiveCalendar
              data={timeline}
              from={timeline[0].day}
              to={timeline[timeline.length - 1].day}
              emptyColor="#eeeeee"
              colors={['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560']}
              margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
              yearSpacing={40}
              monthBorderColor="#ffffff"
              dayBorderWidth={2}
              dayBorderColor="#ffffff"
              legends={[
                {
                  anchor: 'bottom-right',
                  direction: 'row',
                  translateY: 36,
                  itemCount: 4,
                  itemWidth: 42,
                  itemHeight: 36,
                  itemsSpacing: 14,
                  itemDirection: 'right-to-left',
                },
              ]}
            />
          )}
        </div>
      </div>
    );
  }
}

User.propTypes = {
  // redux
  userId: PropTypes.string.isRequired,
  setUserId: PropTypes.func.isRequired,
  userData: PropTypes.object.isRequired,
  setUserData: PropTypes.func.isRequired,
};

const mapStateToProps = (state /* , ownProps */) => {
  return {
    userId: state.user.userId,
    userData: state.user.userData,
  };
};

const mapDispatchToProps = {
  setUserId,
  setUserData,
};

export default connect(mapStateToProps, mapDispatchToProps)(User);
